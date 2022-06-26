from cpu_ldng.config_db import host, user, password, db_name, port
import psycopg2
import psutil
#from cpu_ldng.tasks import start_script_insert_date
#from tasks import start_script_insert_date




cpu_col = psutil.cpu_count()  # кол-во ядер
id = 1

def start_script_delay():
    from .tasks import start_script_insert_date
    start_script_insert_date.delay(1)  # delay запускает функцию в фоне


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




# def stop_script(status):
#     global stat
#     if status == False:
#         stat = False
#     elif stat == False:
#         return False
#     else:
#         return True

# stat = None
# def stop_script(status=True):
#     global stat
#     if status == False:
#         stat = False
#     elif stat == False:
#         return False
#     else:
#         return True




stat = True
def check(status):
    #from delll2 import stat
    global stat
    if status == "False":
        stat = False
    elif stat == False:
        return False
    else:
        return True



def start_script(id):
    #from .tasks import start_script_insert_date
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)

        if id > 10:  # 720*5=3600сек в 1ч  #12*5=60сек (для теста)
            id = 1
        info = psutil.cpu_percent(interval=5, percpu=True)
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE cpu_5sec SET cpu_time = now() WHERE cpu_5sec_id = {id};""")
        for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE cpu_5sec SET cpu_{i} = %s
                    WHERE cpu_5sec_id = {id}; """, [info[i - 1]])
        id += 1
        if check(input()) == True:
            start_script(id)

    except ValueError:
        pass
    finally:
        start_script(id)
        # закрываем подключение к БД
        if connection:
            connection.close()
