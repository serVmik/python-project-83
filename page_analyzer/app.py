import os
from dotenv import load_dotenv
from flask import (
    Flask,
    redirect,
    render_template,
    url_for,
    request,
    flash
)

from page_analyzer import db, urls

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CONN_STRING = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def post_url():
    url_entered = request.form.get('url')
    messages = urls.validate_url(url_entered)

    if messages:
        for message in messages:
            flash(*message)
        return render_template(
            'index.html',
            url=url_entered
        )

    connection = db.connect(CONN_STRING)
    url_name = urls.normalize_url(url_entered)

    if db.is_url_exists(connection, url_name):
        url = db.get_url_by_name(connection, url_name)
        flash('Страница уже существует', 'info')
    else:
        url = db.add_url(connection, url_name)
        flash('Страница успешно добавлена', 'success')

    url_id = url.id
    db.close(connection)

    return redirect(
        url_for(
            'show_url',
            url_id=url_id
        )
    )


@app.get('/urls')
def show_urls():
    connection = db.connect(CONN_STRING)
    urls_ = db.get_urls(connection)
    db.close(connection)

    return render_template(
        'urls.html',
        urls_=urls_
    )


@app.get('/urls/<int:url_id>')
def show_url(url_id):
    connection = db.connect(CONN_STRING)
    url = db.get_url_by_id(connection, url_id)
    url_check = db.get_checks(connection, url_id)
    db.close(connection)

    return render_template(
        'url.html',
        url=url,
        url_check=url_check
    )


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    connection = db.connect(CONN_STRING)
    url = db.get_url_by_id(connection, url_id)
    url_name = url.name
    url_requests = urls.get_page_data(url_name)

    if not url_requests or url_requests.get('status_code') != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check(connection, url_id, url_requests)
        flash('Страница успешно проверена', 'success')

    url_check = db.get_checks(connection, url_id)
    db.close(connection)

    return render_template(
        'url.html',
        url=url,
        url_check=url_check
    )
