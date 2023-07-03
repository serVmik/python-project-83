import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def check_url_for_errors(entered_url, url):
    url_error = []

    if len(entered_url) > 255:
        url_error.append(('URL превышает 255 символов', 'danger'))
    if entered_url == '':
        url_error.append(('URL обязателен', 'danger'))
    if not validators.url(url):
        url_error.append(('Некорректный URL', 'danger'))

    return url_error


def get_requests_info(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        desc = soup.find('meta', attrs={'name': 'description'})
        requests_info = {
            'status_code': r.status_code,
            'h1': soup.h1.get_text().strip() if soup.h1 else '',
            'title': soup.title.string if soup.title else '',
            'description': desc['content'].strip() if desc else ''
        }
        return requests_info

    except requests.ConnectionError:
        return None
