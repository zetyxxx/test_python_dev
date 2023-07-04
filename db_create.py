import psycopg2
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # проверка работоспособности сервера
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")

    # создаем таблицу
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE ttest(
            id serial PRIMARY KEY,
            today DATE,
            func_name VARCHAR(10000),
            args VARCHAR(10000),
            results VARCHAR(10000),
            errors VARCHAR(10000));"""
        )
        print("[INFO] Table created succesfully")


    # with connection.cursor() as cursor:
    #     cursor.execute('''DROP TABLE ttest''')
    #     print("[INFO] Table dropped succesfully")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")