from flask import request, jsonify, render_template, Flask
import sys
import argparse
import json
import os
from importlib.resources import read_text
from cheggscraper import Downloader


app = Flask(__name__, template_folder='')
link = 'https://www.chegg.com/homework-help/questions-and-answers/find-region-integration-2x-4y-1-da-bounded-y-x-2-y-x-3-evaluate-double-integrals-q5681991'

conf = json.loads(read_text('cheggscraper', 'conf.json'))
default_save_file_format = conf.get('default_save_file_format')
default_cookie_file_path = conf.get('default_cookie_file_path')

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def getAnswer():
    input_json = request.args.get('link')
    input_json = str(input_json)
    print("link requested is " + input_json)
    Downloader.main(input_json)
    return "success"