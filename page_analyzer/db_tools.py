import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect():
    return psycopg2.connect(DATABASE_URL)


def is_exists(name):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE name = %s', (name,))
        db_answer = curs.fetchone()
    return True if db_answer else False


def add_url(url):
    conn = connect()
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id',
                     (url,))
        id_, = curs.fetchone()
        conn.commit()
    return id_
