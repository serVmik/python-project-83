from flask import flash
import validators


def validate_url(url):
    error = None

    if len(url) > 255:
        error = True
        flash('URL превышает 255 символов', 'danger')
    if not validators.url(url):
        error = True
        flash('Некорректный URL', 'danger')
    if url == '':
        error = True
        flash('URL обязателен', 'danger')

    return error
