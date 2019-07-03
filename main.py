import os
import sqlite3
import babel
import datetime
import time
import pytz
import dateutil.parser
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_paginate import Pagination, get_page_args
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import babel


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
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/uploads'
print(app.config['UPLOADED_PHOTOS_DEST'])

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

@app.route('/',methods=['GET', 'POST'])
def index():
    error = None
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM user order by first_name')
    users = c.fetchall()
    if request.method == 'POST':
        if request.form['password'].lower() == os.environ['RORO_PASSWORD']:
            session['authorized'] = "true"
            return render_template('index.html', session=session, error=error, users=users)
        else:
            error = 'Invalid password'
    if request.method == 'GET':
        if 'switch' in request.args:
            session['userid'] = 0
        if session['authorized'] == "true" and int(session['userid']) > 0:
            return redirect("/messages", code=302)

    return render_template('index.html', session=session, error=error, users=users)

@app.route('/logout')
def logout():
    session['authorized'] = "false"
    error = 'You have been logged out'
    return render_template('index.html', session=session, error=error)

@app.route('/messages',methods=['GET', 'POST'])
def messages():
    error = None
    page = 1
    if session['authorized'] == "false":
        error = "Bad user id"
    if 'userid' in request.args:
        session['userid'] = request.args.get('userid')
    if not session.get('userid'):
        error = "No user"
    if error:
        return render_template('index.html', session=session, error=error)
        # and so ends the auth and user errors...
    if request.method == 'POST' and 'photo' not in request.files:
        format = '%Y-%m-%dT%H:%M:%S'
        d = datetime.datetime.today()
        d = d.strftime(format)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO MESSAGE('user_id','body','date') VALUES(?,?,?)",  (session.get('userid'),request.form['message'],d))
        conn.commit()
    elif request.method == 'POST' and 'photo' in request.files:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        file = request.files['photo']
        if file.filename == '':
            error = 'No selected file'
        else:
            extension = file.filename.split(".")[-1]
            file.save(os.getcwd() + '/static/uploads/' + st + "." + extension)
            image_tag = '<img style="max-height:100%;max-width:100%;margin:auto;display:block" src="/static/uploads/' + st + '.' + extension + '">'
            print(image_tag)
            format = '%Y-%m-%dT%H:%M:%S'
            d = datetime.datetime.today()
            d = d.strftime(format)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("INSERT INTO MESSAGE('user_id','body','date') VALUES(?,?,?)",(session.get('userid'),image_tag,d))
            conn.commit()

    if 'page' in request.args:
        page = int(request.args.get('page'))
    userid = (session['userid'],)
    offset = ((page * 10) - 10,)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM user where id = ?', userid)
    user = c.fetchone()
    c.execute('SELECT count(*) as total_pages FROM message')
    total_pages = c.fetchone()
    pages = int(total_pages[0] / 10)
    c.execute('SELECT message.id, message.body,message.date,user.id, user.first_name, user.last_name, user.image FROM message,user where message.user_id = user.id order by date desc limit 10 OFFSET ?', offset)
    messages = c.fetchall()
    format = '%Y-%m-%dT%H:%M:%S'
    i = 0
    messages_better_dates = []
    while i < len(messages):
        d = datetime.datetime.strptime(messages[i][2], format)
        d = d.strftime('%B %m %Y at %H:%M')
        list_o_message_values = (messages[i][0], messages[i][1], d, messages[i][3], messages[i][4], messages[i][5], messages[i][6])
        messages_better_dates.append(list_o_message_values)
        i=i+1
    links = ""
    if (page > 1):
        last = page - 1
        links = links + "<a href='/messages?page=" + str(last) + "' class='btn btn-outline-primary'>previous page</a>"
    if ((page / pages) <= 1):
        next = page + 1
        links = links + "&nbsp;&nbsp;<a href='/messages?page=" + str(next) + "' class='btn btn-outline-primary'>next page</a>"

    return render_template('messages.html', session=session, error=error, user=user, messages=messages_better_dates, page=page, links=links)
