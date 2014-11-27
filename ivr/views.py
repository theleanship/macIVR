from ivr import app, db
from ivr import settings
from ivr.decorators import requires_auth
from ivr.models import Call
from flask import render_template, abort, request, make_response, redirect
from flask.views import MethodView
from jinja2.exceptions import TemplateNotFound


def updateCall(args):
    """ make changes to call and save the model """
    if args.get('CallSid'):
        try:
            call = Call.objects.get(callSid=args.get('CallSid'))
        except Call.DoesNotExist():
            # This shouldn't happen, call should exist from incoming url - but just in case:
            call = Call(callSid=args.get('CallSid'),
                        fromNumber=args.get('From'),
                        toNumber=args.get('To'))

    call.duration = args.get('CallDuration')

    if args.get('RecordingUrl'):
        call.recordingUrl = args.get('RecordingUrl')
    if args.get('RecordingSid'):
        call.recordingSid = args.get('RecordingSid')
    if args.get('RecordingDuration'):
        call.recordingDuration = args.get('RecordingDuration')

    call.save()

    return call

@app.route('/listen/<call_id>/', methods=['GET'])
@requires_auth
def listen_voicemail(call_id):
    """ Simple list of recent calls """

    try:
        call = Call.objects.get(callSid=call_id)
        call.listened = True
        call.save()

    except Call.DoesNotExist():
        abort(404)

    return redirect(call.recordingUrl, code=302)


@app.route('/calls/list/', methods=['GET'])
@requires_auth
def call_list():
    """ Simple list of recent calls """

    callList = Call.objects.order_by('-created_at')

    return render_template('calls.html', calls=callList)


@app.route('/call/update/', methods=['POST'])
def status_callback():
    """ Set this url in your twilio account to receive callbacks with call status and recording urls """
    updateCall(request.form)

    return make_response('OK')


@app.route('/voicemail/store/', methods=['POST'])
def store_voicemail():
    """ Callback for the record tag, just returns another twiml script """
    updateCall(request.form)

    twiml = render_template('twiml_voicemail_end.xml')
    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route('/selection/', methods=['POST'])
def selection():
    """ Callback for Gather tag, receieves selected digit and choosing script to respond with """
    if request.form.get('Digits'):
        try:
            twiml = render_template('twiml_select_%s.xml' % request.form.get('Digits'))
        except TemplateNotFound:
            twiml = render_template('twiml_error.xml' % request.form.get('Digits'))

    else:
        abort(400, 'Need some digits')

    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route('/incoming/', methods=['POST'])
def incoming():
    """ The initial route for the call, responds with the first set of twiml / IVR menu """
    # store call in mongo
    newCall = Call(callSid=request.form.get('CallSid'),
                   fromNumber=request.form.get('From'),
                   toNumber=request.form.get('To'))
    newCall.save()

    # return a twiml response
    twiml = render_template('twiml.xml')
    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response
