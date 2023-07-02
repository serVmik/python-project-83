import os
from flask import Flask, redirect, render_template, url_for, request, flash
import page_analyzer.db_tools as db
import page_analyzer.url_tools as url_t

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/url')
def post_url():
    entered_url = request.form.get('url')
    url = url_t.normalize_url(entered_url)

    messages = url_t.check_url_for_errors(entered_url, url)
    if messages:
        [flash(*message) for message in messages]
        return render_template('index.html')

    if db.get_id(url):
        id_ = db.get_id(url)
        flash('Страница уже существует', 'info')
    else:
        id_ = db.add_url_info(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id_=id_))


@app.get('/urls')
def show_urls():
    return render_template('urls.html',
                           urls_info=db.get_urls_info())


@app.get('/urls/<id_>')
def show_url(id_):
    return render_template('url.html',
                           url_info=db.get_url_info(id_),
                           check_info=db.get_check_info(id_))


@app.post('/urls/<id_>/checks')
def check_url(id_):
    url = db.get_url_info(id_).name
    requests_info = url_t.get_requests_info(url)

    if not requests_info:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check_to_url_checks(id_, requests_info)
        flash('Страница успешно проверена', 'success')
    return render_template('url.html',
                           url_info=db.get_url_info(id_),
                           check_info=db.get_check_info(id_))
