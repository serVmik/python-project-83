import os
from flask import Flask, redirect, render_template, url_for, request, flash
from dotenv import load_dotenv
from page_analyzer import db, urls

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CONN_STRING = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_url():
    entered_url = request.form.get('entered_url')
    messages = urls.validate_url(entered_url)
    if messages:
        [flash(*message) for message in messages]
        return render_template('index.html',
                               entered_url=entered_url), 422

    connection = db.connect(CONN_STRING)
    url_name = urls.normalize_url(entered_url)

    if db.is_url_exists(connection, url_name):
        url_id = db.get_url_id(connection, url_name)
        flash('Страница уже существует', 'info')
    else:
        url_id = db.add_url(connection, url_name)
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('show_url',
                            url_id=url_id))


@app.get('/urls')
def show_urls():
    connection = db.connect(CONN_STRING)
    urls_ = db.get_urls(connection)
    return render_template('urls.html',
                           urls_=urls_)


@app.get('/urls/<int:url_id>')
def show_url(url_id):
    connection = db.connect(CONN_STRING)
    url_ = db.get_url(connection, url_id)
    url_checks = db.get_check(connection, url_id)
    return render_template('url.html',
                           url_=url_,
                           url_checks=url_checks)


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

    url_ = db.get_url(connection, url_id)
    url_checks = db.get_check(connection, url_id)
    return render_template('url.html',
                           url_=url_,
                           url_checks=url_checks)
