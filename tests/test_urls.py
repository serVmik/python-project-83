import pytest

from page_analyzer.urls import normalize_url, validate_url
from tests.fixtures.fixtures_urls import (
    give_one_by_one,
    urls_incorrect, url_too_long)


@pytest.mark.parametrize('url_entered, url_name', [
    ('https://ru.hexlet.io/courses/python-basics',
     'https://ru.hexlet.io'),
    ('https://github.com/serVmik/python-project-83',
     'https://github.com'),
    ('https://translate.google.com/?hl=ru&sl=ru&tl=en&op=translate',
     'https://translate.google.com')])
def test_normalize_url(url_entered, url_name):
    url_parsed = normalize_url(url_entered)
    assert url_name == url_parsed


def test_url_empty_and_too_long():
    (message_empty, _) = validate_url('')
    (message_too_long, _) = validate_url(url_too_long)
    assert message_empty == ('URL обязателен', 'danger')
    assert message_too_long == ('URL превышает 255 символов', 'danger')


@pytest.fixture
def urls_incorrect_():
    return urls_incorrect


@give_one_by_one
def test_url_incorrect(urls_incorrect_):
    (message) = validate_url(urls_incorrect_)
    assert message == ('Некорректный URL', 'danger')
