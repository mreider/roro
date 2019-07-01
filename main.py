import os
import gevent
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_limiter.util import get_remote_address
from flask_debugtoolbar import DebugToolbarExtension
from flask import copy_current_request_context
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
app.secret_key = os.environ['RORO_SECRET_KEY'].encode('utf8')
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
error = None
page = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture_url = db.Column(db.String(), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)

@app.route('/',methods=['GET', 'POST'])
def index():
    users = User.query.order_by(User.first_name).all()
    if request.method == 'POST':
        if request.form['password'].lower() == os.environ['RORO_PASSWORD']:
            session['authorized'] = "true"
            return render_template('index.html', session=session, error=error, users=users)
        else:
            error = 'Invalid password'
    return render_template('index.html', session=session, error=error, users=users)


@app.route('/logout')
def logout():
    session['authorized'] = "false"
    error = 'You have been logged out'
    return render_template('index.html', session=session, error=error)

@app.route('/messages')
def messages():
    if session['authorized'] == "false":
        error = "Bad user id"
    if 'userid' in request.args:
        if not isinstance(request.args.get('userid'), int)):
            error = "User id is not a number"
        session['userid'] = request.args.get('userid')
    if not session.get('userid'):
        error = "No user"
    if error:
        return render_template('index.html', session=session, error=error)
        # and so ends the auth and user errors...

    if 'page' in request.args:
        if not isinstance(request.args.get('page'), int)):
            error = "Page is not a number"
            page = 1
        else:
            page = request.args.get('page')
    user = User.query.filter_by(id=session['userid']).first()
    messages = session.query(Message,User).filter(User.id == Message.user_id).order_by(Message.time.desc).paginate(page,15,error_out=False)
    return render_template('messages.html', session=session, error=error, user=user, messages=messages, page=page)
