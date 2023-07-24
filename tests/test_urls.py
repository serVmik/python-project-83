import pytest
from page_analyzer.urls import normalize_url, validate_url


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


@pytest.mark.parametrize('urls_incorrect', [
    ('htp://sorry.jo'), ('http;//just_do.it'), ('http://benq,ru')])
def test_url_incorrect(urls_incorrect,):
    assert ('Некорректный URL', 'danger') in validate_url(urls_incorrect)


def test_url_empty_and_too_long():
    assert ('URL обязателен', 'danger') in validate_url('')
    assert ('URL превышает 255 символов', 'danger') in validate_url('''
    https://itistoooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooolongurl.com''')
