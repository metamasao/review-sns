import requests
import logging

logging.basicConfig(level='DEBUG')

def get_book_info(isbn):
    api_url = 'https://api.openbd.jp/v1/get?isbn='
    api_url += isbn
    logging.debug(api_url)
    response = requests.get(api_url)
    return response.json()[0]