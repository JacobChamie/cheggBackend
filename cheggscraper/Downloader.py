import json
from importlib.resources import read_text

from .CheggScraper import CheggScraper


def main(url):
    conf = json.loads(read_text('cheggscraper', 'conf.json'))

    default_save_file_format = conf.get('default_save_file_format')
    default_cookie_file_path = conf.get('default_cookie_file_path')

    Chegg = CheggScraper(cookie_path=default_cookie_file_path, base_path='templates')
    return Chegg.url_to_html(url, file_name_format=default_save_file_format)