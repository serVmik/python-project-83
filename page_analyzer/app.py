# standard
from flask import (Flask, redirect, render_template, url_for,
                   request, flash)
import os
from dotenv import load_dotenv

# local
from page_analyzer.project_validators import validate_url

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/url')
def get_url():
    return render_template('url.html')


@app.post('/url')
def post_url():
    db = '2'
    url = request.form.get('url', '')
    error = validate_url(url)
    if url in db:
        error = True
        flash('Страница уже существует', 'danger')

    if error:
        return redirect(url_for('index'))
    else:
        flash('Страница успешно добавлена', 'success')
        return render_template('url.html')


@app.get('/urls')
def get_urls():
    return render_template('urls.html')
