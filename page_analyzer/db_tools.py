import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

load_dotenv()


def connect():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


def is_url_exists(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE name = %s', (url,))
        db_answer = curs.fetchone()
        return True if db_answer else False


def add_url_info(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
        id_, = curs.fetchone()
        conn.commit()
        return id_


def get_id(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute(
            'SELECT id FROM urls WHERE name = %s', (url,)
        )
        return curs.fetchone()


def get_norm_url(id_):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('SELECT name FROM urls WHERE id = %s', (id_,))
        norm_url, = curs.fetchone()
        return norm_url


def get_url_info(id_):
    conn = connect()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id = %s', (id_,))
        return curs.fetchone()


def get_urls_info():
    conn = connect()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT urls.id AS id, '
            'urls.name AS name, '
            'url_checks.created_at AS created_at, '
            'url_checks.status_code AS status_code '
            'FROM urls LEFT JOIN url_checks '
            'ON urls.id = url_checks.url_id '
            'AND url_checks.id = ('
            'SELECT max(id) FROM url_checks '
            'WHERE urls.id = url_checks.url_id) '
            'ORDER BY urls.id DESC;'
        )
        return curs.fetchall()


def add_check_to_url_checks(url_id, requests_info):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute(
            'INSERT INTO url_checks '
            '(url_id, status_code, h1, title, description) '
            'VALUES (%s, %s, %s, %s, %s)',
            (url_id,
             requests_info['status_code'],
             requests_info['h1'],
             requests_info['title'],
             requests_info['description'])
        )
        conn.commit()


def get_check_info(id_):
    conn = connect()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT id, status_code, h1, title, description, created_at '
            'FROM url_checks WHERE %s = url_id', (id_,)
        )
        return curs.fetchall()
