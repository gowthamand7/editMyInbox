from flask import Flask, render_template, request, url_for
from flask import session
from werkzeug.utils import redirect

import src.common.utils as utils
from src.models.google import Google

app = Flask(__name__)
app.secret_key = 'testing'


@app.route('/')
def index():
    auth_uri = Google.get_auth_uri()
    return render_template('home.html', url=auth_uri)


@app.route('/google_auth')
def google_auth():
    flow = Google.get_flow()
    if request.args.get('code') is not None:
        credentials = Google.get_credentials(request.args.get('code'))
        credentials_str = "accesstoken: {} \n Refreshtoken: {}".format(credentials.access_token,credentials.refresh_token)
        user_info = Google.get_user_info(credentials)
        user_info_str = utils.dist_to_string(user_info)
        session['user_info'] = "here is the token details {} \n here is the user details {} \n".format(credentials_str,user_info_str)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home')
def home():
    return session['user_info']

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)