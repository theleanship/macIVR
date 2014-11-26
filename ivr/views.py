from ivr import app, db
from ivr import settings
from ivr.models import Call
from flask import render_template, abort, request, make_response, url_for
from flask.views import MethodView
from jinja2.exceptions import TemplateNotFound


class AppView(MethodView):

    def get(self):
        return render_template('messages.html')


def updateCall(args):
    """ make changes to call and save """
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


@app.route('/call/update/', methods=['POST'])
def status_callback():
    """ Set this url in your twilio account to receive callbacks with call status and recording urls """
    updateCall(request.form)

    return make_response('OK')


@app.route('/voicemail/store/', methods=['POST'])
def store_voicemail():
    updateCall(request.form)

    twiml = render_template('twiml_voicemail_end.xml')
    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response

@app.route('/selection/', methods=['POST'])
def selection():
    if request.form.get('Digits'):
        try:
            twiml = render_template('twiml_select_%s.xml' % request.form.get('Digits'),
                                    gather_callback='%s%s' % (settings.SERVER_URL, url_for('selection'),),
                                    voicemail_callback='%s%s' % (settings.SERVER_URL, url_for('store_voicemail'),))
        except TemplateNotFound:
            abort(400, 'No response for that selection')

    else:
        abort(400, 'Need some digits')

    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route('/incoming/', methods=['POST'])
def incoming():
    # store call in mongo
    newCall = Call(callSid=request.form.get('CallSid'),
                   fromNumber=request.form.get('From'),
                   toNumber=request.form.get('To'))
    newCall.save()

    # return a twiml response
    twiml = render_template('twiml.xml', gather_callback='%s%s' % (settings.SERVER_URL, url_for('selection'),))
    response = make_response(twiml)
    response.headers["Content-Type"] = "application/xml"

    return response
