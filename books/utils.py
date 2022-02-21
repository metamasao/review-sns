import requests
import logging

logger = logging.getLogger(__name__)

def get_book_info(isbn):
    api_url = 'https://api.openbd.jp/v1/get?isbn='
    api_url += isbn
    response = requests.get(api_url)
    
    if response.status_code != 200:
        logger.warning('openbd seems to be something wrong')
    return response.json()[0]