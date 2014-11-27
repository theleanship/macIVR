Simple IVR built with flask for guiding callers through an automated support line and taking voicemails. Will also contain a simple UI for reviewing calls and messages.

You will need
- MongoDB
- Twilio

Environment Variables
---------------------

- SERVER_NAME - url to where your app is hosted
- TWILIO_ACCOUNT_SID - twilio details
- TWILIO_AUTH_TOKEN - twilio details
- MONGODB_SETTINGS - a dict containing your mongo config (TBD, probably can't store a dict as an env var!)

Set up Twilio
-------------
On the number you wish to use for the IVR go into the number settings, under voice set:

- Request URL: `http://SERVER_URL /incoming/`
- Status Callback URL: `http://SERVER_URL /call/update/`

Setting up the IVR
------------------

`twiml.xml` contains the xml header/footer with a footer containing a redirect to the beginning of the twiml. This is the starting point for the call where you can list options on the IVR and pass the selected option (digit) through the Gather tag. `{{ url_for('selection', _external=True) }}` is the url for the selection view, set this as the callback for the Gather tag and twiml will send a request with the selected digit to that url. Which loads up the following templates...

`twiml_select_[n].xml` the twiml_select_ templates contain the script for each selection in the IVR. Simply add a template for each selection where [n] is the digit for that option (1,2,3,4,5...). This template extends twiml.xml so it will loop back to the main menu of the IVR when the script finishes.

`twiml_voicemail_end.xml` in twiml_select_3.xml there is an example of using Record to capture voicemails. Use `{{ url_for('store_voicemail', _external=True) }}` variable to set the callback url for Record which will load up the script in this file. 

`twiml_error.xml` a simple script to run on selection errors, where a digit is chosen where there is no option for that digit.



