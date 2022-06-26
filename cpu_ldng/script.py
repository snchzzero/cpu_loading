from cpu_ldng.config_db import host, user, password, db_name, port
import psycopg2
import psutil
from datetime import datetime
import pytz

lasttime = "000"


from cpu_ldng.forms import Form_StartStop
#from cpu_ldng.tasks import start_script_insert_date
#from tasks import start_script_insert_date




cpu_col = psutil.cpu_count()  # кол-во ядер


# def start_script_delay():
#     from .tasks import start_script_insert_date
#     #start_script_insert_date.delay(1)  # delay запускает функцию в фоне
#     start_script_insert_date.delay(1)



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


# после нажатия кнопки старт добавляем даные CPU в таблицу
def start_script():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        if table_IS_NOT_NULL(connection) == True:  # если пустая таблица и все NULL
            id = 1
        else:
            last_id, total_5sec_pause = pause(connection)
        # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
        while True:
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


def pause(connection):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT MAX(cpu_5sec_id), now() - MAX(cpu_time)
                        FROM cpu_5sec WHERE cpu_time IS NOT NULL;"""
                       )
        all = cursor.fetchall()
        last_id = int(all[0][0]) + 1  # id в таблице с которого заполняем поля нулями
        last_time = all[0][1]
        hour, minute, second = last_time.hour, last_time.minute, last_time.second
        total_time = int(((hour * 60 * 60) + (minute * 60) + second) / 5)  # коли-во строк в БД с нулями




def table_IS_NOT_NULL(connection):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) FROM cpu_5sec WHERE cpu_time IS NOT NULL;""")
        if int(cursor.fetchall()[0][0]) == 0:  # целое число
            return True  # если все NULL
        else:
            return False









