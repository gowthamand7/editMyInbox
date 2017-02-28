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

    if next_page_token is not None:
        next_url = '/home/{}'.format(next_page_token)
    else:
        next_url = None

    return render_template('inbox.html', labels=labels, user_info=user_info, messages=messages, next_url=next_url)


@app.route('/label/<string:label_id>')
@app.route('/label/<string:label_id>/<string:next_page_token>')
def label(label_id, next_page_token= None):
    google = Google(flask.session['credentials'])
    user_info = google.get_user_info()
    labels = google.get_labels()
    if next_page_token is None:
        messages, next_page_token = google.get_messages_by_labels(label_id)
    else:
        messages, next_page_token = google.get_messages_by_labels(label_id, page_token=next_page_token)

    if next_page_token is not None:
        next_url = '/label/{}/{}'.format(label_id, next_page_token)
    else:
        next_url = None

    return render_template('inbox.html', labels=labels, user_info=user_info, messages=messages, next_url=next_url)


@app.route('/search')
@app.route('/search/<string:next_page_token>')
def search(next_page_token= None):
    search_query = request.args.get('q')
    google = Google(flask.session['credentials'])
    user_info = google.get_user_info()
    labels = google.get_labels()
    if next_page_token is None:
        messages, next_page_token = google.get_messages_by_subject(search_query=search_query)
    else:
        messages, next_page_token = google.get_messages_by_subject(search_query=search_query, page_token=next_page_token)

    if next_page_token is not None:
        next_url = '/search/{}?q={}'.format(next_page_token,search_query)
    else:
        next_url = None

    return render_template('inbox.html', labels=labels, user_info=user_info, messages=messages, next_url=next_url)


@app.route('/message/<string:message_id>')
def get_message(message_id):
    google = Google(flask.session['credentials'])
    body = google.get_message(message_id)

    return render_template('edit_message.html',body=body)


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True, use_debugger=False, use_reloader=False)
