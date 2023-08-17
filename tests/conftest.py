def drop_tables(connection) -> None:
    with open('./database.sql', 'r') as f:
        query = f.read()
    with connection.cursor() as curs:
        curs.execute(query)
        connection.commit()
