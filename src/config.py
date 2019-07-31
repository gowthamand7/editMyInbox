import os

CLIENT_ID s.googleusercontent.com'
APPLICATION_NAME = 'Edit My Inbox'
SCOPE = 'openid email https://mail.google.com/'
redirect_uri = 'http://127.0.0.1:5000/google_auth'
PATH = os.path.dirname(os.path.abspath(__file__))

MAX_RESULT = 25
