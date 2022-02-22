import requests
import logging

logger = logging.getLogger(__name__)

def get_book_info(isbn):
    api_url = 'https://api.openbd.jp/v1/get?isbn='
    api_url += isbn
    response = requests.get(api_url)
    
    if response.status_code != 200:
        logger.warning('Something seems to be wrong with openbd.')
        return None
    return response.json()[0]