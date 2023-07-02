import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def normalize_url(entered_url):
    parsed_url = urlparse(entered_url)
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
    except requests.ConnectionError:
        return None
    if r.status_code != 200:
        return None

    requests_info = {'status_code': r.status_code}

    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('title'):
        requests_info['title'] = str(soup.find('title').text)
    else:
        requests_info['title'] = ''
    if soup.find('h1'):
        requests_info['h1'] = str(soup.find('h1').text)
    else:
        requests_info['h1'] = ''

    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        requests_info['description'] = description['content'].strip()
    else:
        requests_info['description'] = ''

    return requests_info
