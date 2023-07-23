import pytest

from page_analyzer.urls import validate_url
from tests.fixtures.fixtures_urls import (give_one_by_one,
                                          urls_incorrect, url_too_long)


def test_url_empty():
    (message, _) = validate_url('')
    assert message == ('URL обязателен', 'danger')


def test_url_too_long():
    (message, _) = validate_url(url_too_long)
    assert message == ('URL превышает 255 символов', 'danger')


@pytest.fixture
def urls():
    return urls_incorrect


@give_one_by_one
def test_url_incorrect(urls):
    [(message, _)] = validate_url(urls)
    assert message == 'Некорректный URL'
