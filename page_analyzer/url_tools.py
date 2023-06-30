import validators
from urllib.parse import urlparse


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def check_url_for_errors(url, normalized_url):
    error_url = []

    if len(url) > 255:
        error_url.append(('URL превышает 255 символов', 'danger'))
    if url == '':
        error_url.append(('URL обязателен', 'danger'))
    if not validators.url(normalized_url):
        error_url.append(('Некорректный URL', 'danger'))

    return error_url
