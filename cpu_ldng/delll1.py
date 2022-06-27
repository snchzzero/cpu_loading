from cpu_ldng.config_db import host, user, password, db_name, port
import psycopg2
#import datetime
from datetime import datetime, time
from datetime import timedelta
import psutil
import pytz

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

        for i in range(1, int(cpu_col) + 1):  # добавляем колонки в соответствии с кол-ом ядер
            with connection.cursor() as cursor:
                cursor.execute(f"""ALTER TABLE cpu_5sec ADD COLUMN cpu_{i} real;""")
        # 720*5=3600сек в 1ч  #12*5=60сек (для теста) #721 вставить
        for cpu_5sec_id in range(1, 11):  # формируем пустую таблицу заполненую NULL
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

def start_script():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит



        # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
        id = 1
        for _ in range(3):
            if id > 10:  # 720*5=3600сек в 1ч  #12*5=60сек (для теста)
                id = 1
            info = psutil.cpu_percent(interval=5, percpu=True)
            with connection.cursor() as cursor:
                time_now = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M:%S")
                cursor.execute(f"""UPDATE cpu_5sec SET cpu_time = %s WHERE cpu_5sec_id = {id};""", [time_now])

            for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""UPDATE cpu_5sec SET cpu_{i} = %s
                        WHERE cpu_5sec_id = {id}; """, [info[i - 1]])
            id += 1
    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()


def check_table_not_NULL():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM cpu_5sec WHERE cpu_time IS NOT NULL;""")
            if int(cursor.fetchall()[0][0]) == 0:  # целое число
                return True
            else:
                return False
    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()

def last_id_time():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""SELECT MAX(cpu_5sec_id), MAX(cpu_time)
                            FROM cpu_5sec WHERE cpu_time IS NOT NULL;"""
                           )

            all = cursor.fetchall()
            last_id = int(all[0][0]) + 1  # id в таблице с которого заполняем поля нулями
            last_time = all[0][1]


            time_now = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M:%S")
            pause_time = time(int(time_now.split(':')[0]),
                                int(time_now.split(':')[1]),
                                int(time_now.split(':')[2]))
            pause_time_finish = timedelta(hours=pause_time.hour,
                                 minutes=pause_time.minute,
                                 seconds=pause_time.second)
            pause_time_start = timedelta(hours=last_time.hour,
                                         minutes=last_time.minute,
                                         seconds=last_time.second)
            pause_time = str(pause_time_finish - pause_time_start)
            pause_time = time(int(pause_time.split(':')[0]),
                              int(pause_time.split(':')[1]),
                              int(pause_time.split(':')[2]))



            hour_p, minute_p, second_p = pause_time.hour, pause_time.minute, pause_time.second
            hour_l, minute_l, second_l = last_time.hour, last_time.minute, last_time.second

            last_time_DT = time(hour_l, minute_l, second_l)  # последнее время

            total_time = int(((hour_p * 60 * 60) + (minute_p * 60) + second_p) / 5)  # коли-во строк в БД с нулями

            id = last_id
            for insert in range(total_time):
                if id == 11:  # в случае если достигли конца таблицы #####id==10 заменить для поля на 1час
                    id = 1

                time_old = timedelta(hours=last_time_DT.hour,
                                     minutes=last_time_DT.minute,
                                     seconds=last_time_DT.second)
                time_5sec = timedelta(seconds=5)
                new_time = time_old + time_5sec
                new_time_str = str(new_time)
                last_time_DT = time(int(new_time_str.split(':')[0]),
                                    int(new_time_str.split(':')[1]),
                                    int(new_time_str.split(':')[2]))
                with connection.cursor() as cursor:
                    cursor.execute(f"""UPDATE cpu_5sec 
                                    SET cpu_time = %s
                                     WHERE cpu_5sec_id = {id};""", [new_time])
                    for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""UPDATE cpu_5sec SET cpu_{i} = 0
                                WHERE cpu_5sec_id = {id}; """)
                id += 1
        return id  # возвращаем id с которого продолжим заполнение


    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()

new_connection()
start_script()
#last_id_time()
