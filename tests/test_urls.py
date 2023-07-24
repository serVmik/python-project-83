import pytest
from page_analyzer.urls import normalize_url, validate_url, get_requests


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


@pytest.mark.parametrize('url_incorrect, url_correct', [
    ('htp://sorry.jo', 'https://yandex.ru'),
    ('http;//just_do.it', 'https://ru.hexlet.io'),
    ('http://benq,ru', 'https://github.com')])
def test_validate_url_correct(url_incorrect, url_correct):
    assert ('Некорректный URL', 'danger') in validate_url(url_incorrect)
    assert ('Некорректный URL', 'danger') not in validate_url(url_correct)


def test_validate_url_empty_and_too_long():
    assert ('URL обязателен', 'danger') in validate_url('')
    assert ('URL обязателен', 'danger') not in validate_url('Hi!')
    assert ('URL превышает 255 символов', 'danger') in validate_url('''
    https://itistoooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooolongurl.com''')
    assert ('URL превышает 255 символов', 'danger') not in validate_url(
        'https://itisshorturl.com'
    )


# def test_get_requests():
#     url_requests_expected = {
#         'status_code': 200,
#         'h1': 'h1 found',
#         'title': 'Title found',
#         'description': 'description found'
#     }
#     url_requests = ''
#     assert url_requests == url_requests_expected
