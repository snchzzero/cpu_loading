# from cpu_ldng.config_db import host, user, password, db_name, port
# import psycopg2
# import psutil
# from multiprocessing import *
# import asyncio
# import nest_asyncio
# nest_asyncio.apply()
#
# def new_connection():
#     try:
#         connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name)
#         connection.autocommit = True  # что бы не писать после каждого запроса коммит
#
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT version();")
#             # методо fetchone() возращает либо значание либо None
#             version = cursor.fetchone()
#
#         with connection.cursor() as cursor:
#             cursor.execute("""
#             DROP TABLE IF EXISTS cpu_5sec;""")
#
#         with connection.cursor() as cursor:
#             cursor.execute("""CREATE TABLE IF NOT EXISTS cpu_5sec
#             (
#                 cpu_5sec_id serial,
#                 cpu_time time
#             );""")
#
#         for i in range(1, int(cpu_col) + 1):  # добавляем колонки в соответствии с кол-ом ядер
#             with connection.cursor() as cursor:
#                 cursor.execute(f"""ALTER TABLE cpu_5sec ADD COLUMN cpu_{i} real;""")
#         # 720*5=3600сек в 1ч  #12*5=60сек (для теста) #721 вставить
#         for cpu_5sec_id in range(1, 11):  # формируем пустую таблицу заполненую NULL
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     f"""INSERT INTO cpu_5sec (cpu_5sec_id)
#                         VALUES ({cpu_5sec_id});""")
#     except ValueError:
#         pass
#     finally:
#         # закрываем подключение к БД
#         if connection:
#             connection.close()
#
# new_connection()