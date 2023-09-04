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

from page_analyzer import db, html

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def post_url():
    url_entered = request.form.get('url')
    messages = html.validate_url(url_entered)

    if messages:
        for message in messages:
            flash(*message)
        return render_template(
            'index.html',
            url=url_entered,
        ), 422

    connection = db.connect(app)
    url_name = html.normalize_url(url_entered)
    url = db.get_url_by_name(connection, url_name)

    if url:
        flash('Страница уже существует', 'info')
    else:
        url = db.add_url(connection, url_name)
        flash('Страница успешно добавлена', 'success')

    db.close(connection)

    return redirect(
        url_for(
            'show_url',
            url_id=url.id,
        )
    )


@app.get('/urls')
def show_urls():
    connection = db.connect(app)
    urls = db.get_urls(connection)
    db.close(connection)

    return render_template(
        'urls.html',
        urls=urls,
    )


@app.get('/urls/<int:url_id>')
def show_url(url_id):
    connection = db.connect(app)
    url = db.get_url_by_id(connection, url_id)
    url_checks = db.get_checks(connection, url_id)
    db.close(connection)

    return render_template(
        'url.html',
        url=url,
        url_checks=url_checks,
    )


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    connection = db.connect(app)
    url = db.get_url_by_id(connection, url_id)
    page_data = html.get_page_data(url.name)

    if not page_data or page_data.get('status_code') != 200:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        db.add_check(connection, url_id, page_data)
        flash('Страница успешно проверена', 'success')

    url_checks = db.get_checks(connection, url_id)
    db.close(connection)

    return render_template(
        'url.html',
        url=url,
        url_checks=url_checks,
    )
