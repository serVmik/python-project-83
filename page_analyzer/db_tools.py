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


def add_url_information(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
        id_, = curs.fetchone()
        conn.commit()
        return id_


def get_id(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (url,))
        id_, = curs.fetchone()
        return id_


def get_url_information(id_):
    conn = connect()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id = %s', (id_,))
        return curs.fetchone()


def show_added_urls():
    conn = connect()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT id, name FROM urls ORDER BY created_at DESC')
        return curs.fetchall()
