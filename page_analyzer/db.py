import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect(conn_string):
    return psycopg2.connect(conn_string)


def is_url_exists(connection, url_name):
    with connection.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE name = %s', (url_name,))
        db_answer = curs.fetchone()
        return True if db_answer else False


def add_url(connection, url_name):
    with connection.cursor() as curs:
        curs.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id', (url_name,)
        )
        url_id, = curs.fetchone()
        connection.commit()
        return url_id


def get_url_id(connection, url_name):
    with connection.cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (url_name,))
        url_id, = curs.fetchone()
        return url_id


def get_url(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        return curs.fetchone()


def get_urls(connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
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


def add_check(connection, url_id, requests_info):
    with connection.cursor() as curs:
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
        connection.commit()


def get_check(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT '
            'id AS check_id, status_code, h1, title, description, created_at '
            'FROM url_checks WHERE %s = url_id', (url_id,)
        )
        return curs.fetchall()
