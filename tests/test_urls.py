import pytest

from page_analyzer.urls import normalize_url, validate_url


@pytest.mark.parametrize(
    'url_entered, url_name',
    [
        ('https://ru.hexlet.io/courses/python-basics',
         'https://ru.hexlet.io'),
        ('https://translate.google.com/?hl=ru&sl=ru&tl=en&op=translate',
         'https://translate.google.com'),
    ]
)
def test_normalize_url(url_entered, url_name):
    url_parsed = normalize_url(url_entered)
    assert url_name == url_parsed


class TestValidateUrl:
    urls = [
        ('htp://sorry.jo', 'https://yandex.ru'),
        ('http://benq,ru', 'https://github.com'),
    ]
    empty_url = ''
    not_empty_url = 'https://mail.ru'
    too_long_url = 'o' * 256
    short_url = 'https://itisshorturl.com'

    @pytest.mark.parametrize('url_incorrect, url_correct', urls)
    def test_validate_incorrect_url(self, url_incorrect, url_correct):
        assert ('Некорректный URL', 'danger') in validate_url(url_incorrect)
        assert ('Некорректный URL', 'danger') not in validate_url(url_correct)

    def test_validate_empty_url(self):
        assert ('URL обязателен', 'danger') in validate_url(self.empty_url)
        assert ('URL обязателен', 'danger') not in validate_url(self.not_empty_url)

    def test_validate_too_long_url(self):
        assert ('URL превышает 255 символов', 'danger') in validate_url(self.too_long_url)
        assert ('URL превышает 255 символов', 'danger') not in validate_url(self.short_url)
