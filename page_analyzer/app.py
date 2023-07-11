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
        id_ = db.get_url_id(url)
        flash('Страница уже существует', 'info')
    else:
        id_ = db.add_url(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id_=id_))


@app.get('/urls')
def show_urls():
    return render_template('urls.html',
                           urls_info=db.get_urls())


@app.get('/urls/<int:id_>')
def show_url(id_):
    return render_template('url.html',
                           url_info=db.get_url(id_),
                           check_info=db.get_check(id_))


@app.post('/urls/<int:id_>/checks')
def check_url(id_):
    url = db.get_url(id_).name
    requests_info = urls.get_requests(url)

    if not requests_info or requests_info.get('status_code') != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check(id_, requests_info)
        flash('Страница успешно проверена', 'success')
    return render_template('url.html',
                           url_info=db.get_url(id_),
                           check_info=db.get_check(id_))
