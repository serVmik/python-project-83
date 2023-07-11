import os
from flask import Flask, redirect, render_template, url_for, request, flash
from page_analyzer import db, urls

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


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

    if db.is_url_exists(url):
        url_id = db.get_url_id(url)
        flash('Страница уже существует', 'info')
    else:
        url_id = db.add_url(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', url_id=url_id))


@app.get('/urls')
def show_urls():
    return render_template('urls.html',
                           urls_info=db.get_urls())


@app.get('/urls/<int:url_id>')
def show_url(url_id):
    return render_template('url.html',
                           url_info=db.get_url(url_id),
                           check_info=db.get_check(url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    url = db.get_url(url_id).name
    requests_info = urls.get_requests(url)

    if not requests_info or requests_info.get('status_code') != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check(url_id, requests_info)
        flash('Страница успешно проверена', 'success')
    return render_template('url.html',
                           url_info=db.get_url(url_id),
                           check_info=db.get_check(url_id))
