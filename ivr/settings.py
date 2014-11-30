import os

def get_var_or(var, default=None):
	return os.environ.get(var) or default

SERVER_NAME = get_var_or('SERVER_NAME', "http://localhost:8000")
TWILIO_ACCOUNT_SID = get_var_or('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = get_var_or('TWILIO_AUTH_TOKEN')
MONGODB_DBNAME = get_var_or('MONGODB_DBNAME', "macivr")
MONGODB_HOST = get_var_or('MONGODB_HOST', '127.0.0.1')
FRONTEND_USERNAME = get_var_or('FRONTEND_USERNAME', 'macivr')
FRONTEND_PASSWORD = get_var_or('FRONTEND_PASSWORD', 'Pa55w0rd')