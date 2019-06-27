import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_debugtoolbar import DebugToolbarExtension
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
app.secret_key = os.environ['RORO_SECRET_KEY'].encode('utf8')
toolbar = DebugToolbarExtension(app)
@app.route('/',methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['password'].lower() == os.environ['RORO_PASSWORD']:
            session['authorized'] = True
            return render_template('index.html', session=session, error=error)
        else:
            error = 'Invalid password'
    return render_template('index.html', session=session, error=error)
