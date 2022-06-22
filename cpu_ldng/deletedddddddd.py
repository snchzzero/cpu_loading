from config_db import host, user, password, db_name, port
import psycopg2
import psutil

cpu_col = psutil.cpu_count()  # кол-во ядер

def new_connection():
    try:


        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            # методо fetchone() возращает либо значание либо None
            version = cursor.fetchone()

        with connection.cursor() as cursor:
            cursor.execute("""
            DROP TABLE IF EXISTS cpu_5sec;""")

        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS cpu_5sec
            (
                cpu_5sec_id serial,
                cpu_time time    
            );""")

        for i in range(1, int(cpu_col) + 1):
            with connection.cursor() as cursor:
                cursor.execute(f"""ALTER TABLE cpu_5sec ADD COLUMN cpu_{i} real;""")
        for cpu_5sec_id in range(1, 11):
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO cpu_5sec (cpu_5sec_id)
                        VALUES ({cpu_5sec_id});""")

    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()


def script(flag):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
        id = 1
        while flag == True: #720*5=3600сек в 1ч  #12*5=60сек (для теста)
            if id <= 10: #720*5=3600сек в 1ч  #12*5=60сек (для теста)
                info = psutil.cpu_percent(interval=5, percpu=True)
                with connection.cursor() as cursor:
                    cursor.execute(f"""UPDATE cpu_5sec SET cpu_time = now() WHERE cpu_5sec_id = {id};""")
                for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""UPDATE cpu_5sec SET cpu_{i} = %s 
                            WHERE cpu_5sec_id = {id}; """, [info[i-1]])
                id += 1
            else:
                id = 1

    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()












new_connection()
script(True)