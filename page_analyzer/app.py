import os
from flask import (Flask, redirect, render_template, url_for, request, flash)
from page_analyzer.db_tools import (add_url_info, get_urls_info, get_id,
                                    get_url_info, is_url_exists,
                                    add_check_to_url_checks, get_check_info)
from page_analyzer.url_tools import check_url_for_errors, normalize_url

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/url')
def post_url():
    url = request.form.get('url')
    norm_url = normalize_url(url)

    messages = check_url_for_errors(url, norm_url)
    if messages:
        [flash(*message) for message in messages]
        return render_template('index.html')

    if is_url_exists(norm_url):
        id_ = get_id(norm_url)
        flash('Страница уже существует', 'info')
    else:
        id_ = add_url_info(norm_url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id_=id_))


@app.get('/urls/<id_>')
def get_url(id_):
    return render_template('url.html', url_info=get_url_info(id_))


@app.get('/urls')
def get_urls():
    return render_template('urls.html', urls_info=get_urls_info())


@app.post('/urls/<id_>/checks')
def check_url(id_):
    add_check_to_url_checks(id_)
    return render_template('url.html', url_info=get_url_info(id_),
                           check_info=get_check_info(id_))
