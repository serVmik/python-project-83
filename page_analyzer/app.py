import os
from flask import Flask, redirect, render_template, url_for, request, flash
from dotenv import load_dotenv
from page_analyzer import db, urls

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

load_dotenv()
CONN_STRING = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/url')
def post_url():
    entered_url = request.form.get('url')
    url = urls.normalize_url(entered_url)

    messages = urls.validate_url(entered_url, url)
    if messages:
        [flash(*message) for message in messages]
        return redirect(url_for('index'))

    connection = db.connect(CONN_STRING)
    if db.is_url_exists(connection, url):
        url_id = db.get_url_id(connection, url)
        flash('Страница уже существует', 'info')
    else:
        url_id = db.add_url(connection, url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url',
                            url_id=url_id))


@app.get('/urls')
def show_urls():
    connection = db.connect(CONN_STRING)
    urls_info = db.get_urls(connection)
    return render_template('urls.html',
                           urls_info=urls_info)


@app.get('/urls/<int:url_id>')
def show_url(url_id):
    connection = db.connect(CONN_STRING)
    url_info = db.get_url(connection, url_id)
    check_info = db.get_check(connection, url_id)
    return render_template('url.html',
                           url_info=url_info,
                           check_info=check_info)


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    connection = db.connect(CONN_STRING)
    url = db.get_url(connection, url_id).name
    requests_info = urls.get_requests(url)

    if not requests_info or requests_info.get('status_code') != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check(connection, url_id, requests_info)
        flash('Страница успешно проверена', 'success')
    url_info = db.get_url(connection, url_id)
    check_info = db.get_check(connection, url_id)
    return render_template('url.html',
                           url_info=url_info,
                           check_info=check_info)
