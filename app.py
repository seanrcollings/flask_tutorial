from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__) # instane of our app
app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///' +
                  os.path.join(basedir, 'app.db'), # defined location of db file
                  SQLALCHEMY_TRACK_MODIFICATIONS=False)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Message # must be imported after the db is declared, otherwie ImportError

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Message': Message}

# pylint: disable=no-member
@app.route('/', methods=["GET", "POST"]) # routes are defined using decorators
def home():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return render_template('index.html', num=request.form['num']) # pass context to the Jinja template for rendering

@app.route("/messages")
def messages():
    messages = Message.query.all() # FROM message SELECT *;
    return render_template('messages.html', messages=messages)

@app.route("/messages/new", methods=['GET', 'POST'])
def new_message():
    if request.method == 'GET':
        return render_template('message_new.html')
    elif request.method == 'POST':
        message = Message(text=request.form['message'])
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('thing', user='jaren', year='2020', month=1, day=1))

@app.route("/messages/<int:_id>")
def show_message(_id):
    message = Message.query.get(_id)
    return render_template("message_show.html", message=message)