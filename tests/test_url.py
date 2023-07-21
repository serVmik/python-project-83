import pytest
from page_analyzer.urls import validate_url


def test_url_required():
    (validated_url, _) = validate_url('')
    assert validated_url == ('URL обязателен', 'danger')
