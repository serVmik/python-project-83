import validators
from urllib.parse import urlparse
import requests


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def check_url_for_errors(url, norm_url):
    url_error = []

    if len(url) > 255:
        url_error.append(('URL превышает 255 символов', 'danger'))
    if url == '':
        url_error.append(('URL обязателен', 'danger'))
    if not validators.url(norm_url):
        url_error.append(('Некорректный URL', 'danger'))

    return url_error


def get_req_info(norm_url):
    r = requests.get(norm_url)
    return {'status_code': r.status_code}
