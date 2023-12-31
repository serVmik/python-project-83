import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def normalize_url(url):
    url_parsed = urlparse(url)
    return f'{url_parsed.scheme}://{url_parsed.netloc}'


def validate_url(url_entered):
    url_errors = []

    if len(url_entered) > 255:
        url_errors.append(('URL превышает 255 символов', 'danger'))
    if url_entered == '':
        url_errors.append(('URL обязателен', 'danger'))
    if not validators.url(url_entered):
        url_errors.append(('Некорректный URL', 'danger'))

    return url_errors


def get_page_data(url_name):
    try:
        r = requests.get(url_name)
        soup = BeautifulSoup(r.text, 'html.parser')
        desc = soup.find('meta', attrs={'name': 'description'})
        page_data = {
            'status_code': r.status_code,
            'h1': soup.h1.get_text().strip() if soup.h1 else '',
            'title': soup.title.string if soup.title else '',
            'description': desc['content'].strip() if desc else ''
        }
        return page_data

    except requests.ConnectionError:
        return None
