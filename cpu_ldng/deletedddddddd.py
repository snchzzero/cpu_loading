# from cpu_ldng.config_db import host, user, password, db_name, port
# import psycopg2
# import psutil
#
# # from multiprocessing import *
# # import asyncio
# # import time
# # import nest_asyncio
# # nest_asyncio.apply()
#
# cpu_col = psutil.cpu_count()  # кол-во ядер
#
#
# # def start_process(flag):  # Запуск Process
# #     if flag == True:
# #         global p1
# #         p1 = Process(target=start_script, args=()).start()
# #     elif flag == False:
# #         try:
# #             outs, errs = p1.communicate(timeout=15)
# #         except ValueError:
# #             p1.kill()
# #             outs, errs = p1.communicate()
#
# # async def start_process(flag):
# #     await start_script(flag)
#
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
#
# # после нажатия кнопки старт добавляем даные CPU в таблицу
#
# stat = True
#
#
# def stop_script(status):
#     global stat
#     if status == 'False':
#         stat = False
#         return True
#     elif stat == False:
#         return False
#     else:
#         return True
#
#
# def check(flag):
#     return stop_script(input())
#
#
# def start_script():
#     try:
#         connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name)
#         connection.autocommit = True  # что бы не писать после каждого запроса коммит
#
#         # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
#         id = 1
#         flag = True
#         # while flag == True:
#         # total = 0
#         while flag == True:
#             # while total < 10:
#             if id <= 10:  # 720*5=3600сек в 1ч  #12*5=60сек (для теста)
#                 info = psutil.cpu_percent(interval=5, percpu=True)
#                 with connection.cursor() as cursor:
#                     cursor.execute(f"""UPDATE cpu_5sec SET cpu_time = now() WHERE cpu_5sec_id = {id};""")
#                 for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
#                     with connection.cursor() as cursor:
#                         cursor.execute(
#                             f"""UPDATE cpu_5sec SET cpu_{i} = %s
#                             WHERE cpu_5sec_id = {id}; """, [info[i - 1]])
#                 id += 1
#                 # total += 1
#                 flag = check(True)
#             else:
#                 id = 1
#
#
#
#     except ValueError:
#         pass
#     finally:
#         # закрываем подключение к БД
#         if connection:
#             connection.close()
#
#
# new_connection()
# start_script()

# loop = asyncio.get_event_loop()
# #loop.run_until_complete(start_script())
# asyncio.ensure_future(start_script())
# loop.run_forever()


#####################

# from cpu_ldng.config_db import host, user, password, db_name, port
# import psycopg2
# import psutil
# from .tasks import start_script_insert_date
#
# cpu_col = psutil.cpu_count()  # кол-во ядер
# id = 1
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
# #после нажатия кнопки старт добавляем даные CPU в таблицу
#
# stat = None
# def stop_script(status):
#     global stat
#     if status == False:
#         stat = False
#     elif stat == False:
#         return False
#     else:
#         return True
#
# def check(flag):
#     return stop_script(flag)
#
#
# def start_script_delay():
#     global id
#     start_script_insert_date.delay()  # delay запускает функцию в фоне
#
# def start_script():
#     try:
#         connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name)
#         connection.autocommit = True  # что бы не писать после каждого запроса коммит
#
#         # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
#         flag = True
#         if id > 10:  #720*5=3600сек в 1ч  #12*5=60сек (для теста)
#             id = 1
#
#         info = psutil.cpu_percent(interval=5, percpu=True)
#         with connection.cursor() as cursor:
#             cursor.execute(f"""UPDATE cpu_5sec SET cpu_time = now() WHERE cpu_5sec_id = {id};""")
#         for i in range(1, int(cpu_col) + 1):  # добавляем данные в колонки в соответствии с кол-ом ядер
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     f"""UPDATE cpu_5sec SET cpu_{i} = %s
#                     WHERE cpu_5sec_id = {id}; """, [info[i - 1]])
#             id += 1
#
#             # if check(True) != False:
#             #     start_script_insert_date.delay()
#
#
#     except ValueError:
#         pass
#     finally:
#         # закрываем подключение к БД
#         if connection:
#             connection.close()