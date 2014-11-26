Simple IVR built with flask for guiding callers through an automated support line and taking voicemails. Will also contain a simple UI for reviewing calls and messages.

You will need
- MongoDB
- Twilio

Environment Variables
---------------------

- SERVER_URL - url to where your app is hosted
- TWILIO_ACCOUNT_SID - twilio details
- TWILIO_AUTH_TOKEN - twilio details
- MONGODB_SETTINGS - a dict containing your mongo config (TBD, probably can't store a dict as an env var!)

Set up Twilio
-------------
On the number you wish to use for the IVR go into the number settings, under voice set:

- Request URL: `http://SERVER_URL /incoming/`
- Status Callback URL: `http://SERVER_URL /call/update/`


