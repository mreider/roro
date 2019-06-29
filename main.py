import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_limiter.util import get_remote_address
from flask_debugtoolbar import DebugToolbarExtension
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
app.secret_key = os.environ['RORO_SECRET_KEY'].encode('utf8')
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)


@app.route('/',methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['password'].lower() == os.environ['RORO_PASSWORD']:
            session['authorized'] = True
            users = User.query.order_by(User.first_name).all()
            return render_template('index.html', session=session, error=error, users=users)
        else:
            error = 'Invalid password'
    return render_template('index.html', session=session, error=error)
