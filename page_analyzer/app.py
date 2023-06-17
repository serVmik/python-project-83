from flask import Flask, render_template

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    return render_template('urls.html')


@app.get('/report')
def get_report():
    return render_template('report.html')


@app.post('/report')
def post_report():
    return render_template('report.html')
