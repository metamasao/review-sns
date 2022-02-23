import requests
import logging

logger = logging.getLogger(__name__)

def get_book_info(isbn):
    api_url = f'https://api.openbd.jp/v1/get?isbn={isbn}'
    response = requests.get(api_url)
    if response.status_code != 200:
        logger.warning('Something seems to be wrong with openbd.')
        return None
    
    response_data = response.json()[0]
    if response_data is None:
        return None
    return response_data.get('summary')