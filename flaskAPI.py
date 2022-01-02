from flask import render_template, Flask, request
import json
from importlib.resources import read_text
from cheggscraper import Downloader
import logging
import sys


app = Flask(__name__, template_folder='templates')
link = 'https://www.chegg.com/homework-help/questions-and-answers/find-region-integration-2x-4y-1-da-bounded-y-x-2-y-x-3-evaluate-double-integrals-q5681991'

parseAnswer = ""


conf = json.loads(read_text('cheggscraper', 'conf.json'))
default_save_file_format = conf.get('default_save_file_format')
default_cookie_file_path = conf.get('default_cookie_file_path')



@app.route('/')
def my_form():
    return render_template('index.html')
@app.route('/Page-1.html')
def buyPage():
    return render_template('Page-1.html')
@app.route('/', methods=['GET'])
def urlLink():
    url = request.form['urlBox']
    parseAnswer = Downloader.main(url)
    parseAnswer = str(parseAnswer)[10:]
    return render_template(parseAnswer)
@app.route('/get', methods=['GET'])
def getAnswer():
    input_json = request.args.get('link')
    parseAnswer = Downloader.main(input_json)
    parseAnswer = str(parseAnswer)[10:]
    return render_template(parseAnswer)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)