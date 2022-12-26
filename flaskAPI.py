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
app.secret_key = 'super secret string'
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
    username = request.args.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    return user
@app.route('/')
@flask_login.login_required
def my_form():
    return render_template('index.html')
@app.route('/Page-1.html')
@flask_login.login_required
def buyPage():
    return render_template('Page-1.html')
@app.route('/login.html', methods=['GET', 'POST'])
def loginPage():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    username = request.args.get['username']
    password = request.args.get['password']
    if username in users and password == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('Page-1.html'))
    return 'Bad login'
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
    return "Website under maintenence :), please return to previous page", 500