import os

def get_var_or(var, default=None):
	return os.environ.get(var) or default

SERVER_NAME = get_var_or('SERVER_NAME', "http://localhost:8000")
TWILIO_ACCOUNT_SID = get_var_or('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = get_var_or('TWILIO_AUTH_TOKEN')
MONGODB_SETTINGS = get_var_or('MONGODB_SETTINGS', {'DB': "macivr"})