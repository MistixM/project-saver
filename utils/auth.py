from functools import wraps
from flask import request, Response, session

from datetime import datetime, timedelta

from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

SESSION_TIMEOUT = timedelta(minutes=30)

def check_auth(username, password):
    return username == parser['AUTH']['username'] and password == parser['AUTH']['password']

def authenticate():
    return Response("Could not verify your access level.\n"
                    "You have to login with proper credentials", 401,
                    {"WWW-Authenticate": "Basic realm='Login Required'"})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        now = datetime.now()
        last_activity = session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.fromisoformat(last_activity)
            
            if now - last_activity_time > SESSION_TIMEOUT:
                session.clear()
                return authenticate()
        
        session['last_activity'] = now.isoformat()
        return f(*args, **kwargs)
    return decorated

def get_session_token():
    return parser['AUTH']['session_key']