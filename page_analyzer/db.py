import psycopg2
from psycopg2.extras import NamedTupleCursor, DictCursor


def connect(app):
    return psycopg2.connect(
        app.config['DATABASE_URL'],
    )


def close(connection):
    return connection.close()


def add_url(connection, url_name):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''
            INSERT INTO urls (name)
            VALUES (%s) RETURNING id
            ''',
            (url_name,)
        )
        url = curs.fetchone()
        connection.commit()

        return url


def add_check(connection, url_id, page_data):
    with connection.cursor() as curs:
        curs.execute(
            '''
            INSERT INTO url_checks
            (url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (url_id,
             page_data['status_code'],
             page_data['h1'],
             page_data['title'],
             page_data['description'])
        )
        connection.commit()


def get_url_by_name(connection, url_name):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''
            SELECT id, name, created_at
            FROM urls
            WHERE name = %s
            ''',
            (url_name,)
        )
        url = curs.fetchone()

        return url if url else None


def get_url_by_id(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''
            SELECT id, name, created_at
            FROM urls
            WHERE id = %s
            ''',
            (url_id,)
        )
        url = curs.fetchone()

        return url


def get_checks(connection, url_id):
    with connection.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            '''
            SELECT id AS check_id,
                   status_code,
                   h1,
                   title,
                   description,
                   last_checked_at
            FROM url_checks
            WHERE %s = url_id
            ''', (url_id,)
        )
        checks = curs.fetchall()

        return checks


def get_urls(connection):
    with connection.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            '''
            SELECT id,
                   name
            FROM urls
            '''
        )
        urls = curs.fetchall()

    check_urls = []
    last_check_index = -1

    for url in urls:
        checks = get_checks(connection, url.get('id'))
        latest_check = checks[last_check_index] if checks else {}

        url = dict(url)
        url['last_checked_at'] = latest_check.get('last_checked_at', '')
        url['status_code'] = latest_check.get('status_code', '')
        check_urls.insert(last_check_index, url)

    return check_urls
