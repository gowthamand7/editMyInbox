import uuid

import flask
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from src.models.google import Google

app = Flask(__name__)


@app.route('/')
def index():
    auth_uri = Google.get_auth_uri()
    return render_template('home.html', url=auth_uri)


@app.route('/google_auth')
def google_auth():
    flow = Google.get_flow()
    if request.args.get('code') is not None:
        credentials = Google.get_credentials(request.args.get('code'))
        flask.session['credentials'] = credentials.to_json()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home/<string:next_page_token>')
@app.route('/home')
def home(next_page_token= None):
    google = Google(flask.session['credentials'])
    user_info = google.get_user_info()
    labels = google.get_labels()
    if next_page_token is None:
        messages, next_page_token = google.get_messages()
    else:
        messages, next_page_token = google.get_messages(page_token=next_page_token)
    return render_template('inbox.html', labels=labels, user_info=user_info, messages=messages, nextPageToken=next_page_token)

if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True, use_debugger=False, use_reloader=False)
