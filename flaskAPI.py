from flask import render_template, Flask, request, redirect, url_for
import json
from importlib.resources import read_text
from cheggscraper import Downloader
import logging
import sys
from cheggscraper import *
import flask_login
import flask

app = Flask(__name__, template_folder='templates')
link = 'https://www.chegg.com/homework-help/questions-and-answers/find-region-integration-2x-4y-1-da-bounded-y-x-2-y-x-3-evaluate-double-integrals-q5681991'

parseAnswer = ""


conf = json.loads(read_text('cheggscraper', 'conf.json'))
default_save_file_format = conf.get('default_save_file_format')
default_cookie_file_path = conf.get('default_cookie_file_path')

users = {'admin': {'password': 'admin'}}
login_manager = flask_login.LoginManager()
app = flask.Flask(__name__)
app.secret_key = '8FE9384CB47FE9327FD175EED1449'
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@app.route('/')
@flask_login.login_required
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if flask.request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if username in users and password == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('homepage'))
    return 'Bad login'

@app.route('/Page-1')
@flask_login.login_required
def buyPage():
    return render_template('Page-1.html')

@app.route('/urlBox')
@flask_login.login_required
def urlLink():
    url = request.args.get('urlBox')
    parseAnswer = Downloader.main(url)
    parseAnswer = str(parseAnswer)[10:]
    return render_template(parseAnswer)

@app.route('/get', methods=['GET'])
@flask_login.login_required
def getAnswer():
    input_json = request.args.get('link')
    parseAnswer = Downloader.main(input_json)
    parseAnswer = str(parseAnswer)[10:]
    return render_template(parseAnswer)

@app.errorhandler(Exception)
def all_exception_handler(error):
    return "Exception Occurred: " + str(error)

@login_manager.unauthorized_handler
def handle_needs_login():
    flask.flash('You need to login first.')
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'