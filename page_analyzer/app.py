from flask import (Flask, redirect, render_template, url_for,
                   request, flash, get_flashed_messages)
import os
import validators

from page_analyzer import db_tools, url_tools

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/url')
def get_url():
    return render_template('url.html')


@app.post('/url')
def post_url():
    url = request.form.get('url')
    normalized_url = url_tools.normalize_url(url)
    error_url = None

    if len(url) > 255:
        flash('URL превышает 255 символов', 'danger')
        error_url = True
    if url == '':
        flash('URL обязателен', 'danger')
        error_url = True
    if not validators.url(normalized_url):
        flash('Некорректный URL', 'danger')
        error_url = True
    if db_tools.is_exists(normalized_url):
        flash('Страница уже существует', 'danger')
        error_url = True

    if error_url:
        return render_template('index.html')

    db_tools.add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return render_template('url.html')


@app.get('/urls')
def get_urls():
    return render_template('urls.html')
