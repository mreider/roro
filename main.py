from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request
app = Flask(__name__)
app.secret_key = 'foo0bar0buzz'.encode('utf8')

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html',session=session)
