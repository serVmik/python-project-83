import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect(conn_string):
    return psycopg2.connect(conn_string)


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


def get_urls(connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            '''
            SELECT urls.id AS id,
                   urls.name AS name,
                   url_checks.last_checked_at AS last_checked_at,
                   url_checks.status_code AS status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            AND url_checks.id =
              (SELECT max(id)
               FROM url_checks
               WHERE urls.id = url_checks.url_id)
            ORDER BY urls.id DESC;
            '''
        )
        urls = curs.fetchall()

        return urls


def get_checks(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
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
