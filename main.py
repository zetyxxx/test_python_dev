from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import numpy as np

import psycopg2
from config import host, user, password, db_name

import datetime
import inspect

# Функция для получения имени выполняемой функции
def get_func_name():
    frame = inspect.currentframe()
    name = frame.f_back.f_code.co_name
    return name

# Косметическое преобразование данных для записи в БД
def get_args(var):
    arg = ''
    for i in var:
        arg += (str(i) + ', ')
    return arg[:-2]

# Выделенная абстракция
def write_to_db(func_name, args, results=None, errors=None):
    connection = psycopg2.connect(
        host="db",
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    current_date = datetime.date.today()

    if errors == None:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE ttest(
                id serial PRIMARY KEY,
                today DATE,
                func_name VARCHAR(10000),
                args VARCHAR(10000),
                results VARCHAR(10000),
                errors VARCHAR(10000));""")

        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO ttest (today, func_name, args, results) VALUES 
                (%s, %s, %s, %s);''', (current_date, func_name, args, results)
            )
            print("[INFO] success")

    elif errors != None:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO ttest (today, func_name, args, errors) VALUES 
                (%s, %s, %s, %s);''', (current_date, func_name, args, errors)
            )
            print("[INFO] Error while working with PostgreSQL", errors)

    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")

# Мэйн функция
def polinom(y, x, k):
    x = np.array(x)
    arg_x = get_args(x)
    y = np.array(y)
    arg_y = get_args(y)
    input_data = (f'x: {arg_x} \ny: {arg_y} \ndegree: {k}')

    try:
        func_name = get_func_name()

        poly = PolynomialFeatures(degree=k, include_bias=False)
        X = poly.fit_transform(x.reshape(-1, 1))
        model = LinearRegression()
        model.fit(X, y)

        res = f'intercept: {model.intercept_} \ncoefs: {get_args(model.coef_)} \npredicted: {get_args(model.predict(X))}'

        write_to_db(func_name, input_data, results=res)


    except Exception as _ex:
        write_to_db(func_name, input_data, errors=str(_ex))

        print("[INFO] Error while working with PostgreSQL", _ex)

    return model.predict(X), model.intercept_, model.coef_





