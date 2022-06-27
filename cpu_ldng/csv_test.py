from cpu_ldng.config_db import host, user, password, db_name, port
import csv
import psycopg2
import psutil

#графики
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

cpu_col = psutil.cpu_count()  # кол-во ядер

def test():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
        connection.autocommit = True  # что бы не писать после каждого запроса коммит

        with connection.cursor() as cursor:

            cursor.execute("""SELECT * FROM cpu_5sec ORDER BY cpu_5sec_id;""")
            all = cursor.fetchall()
            return all

    except ValueError:
        pass
    finally:
        # закрываем подключение к БД
        if connection:
            connection.close()

def csv_w():
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        data = test()
        ROW =  ['cpu_5sec_id', 'cpu_time']
        for i in range(1, int(cpu_col) + 1):
            ROW.append(f'cpu_{i}')
        writer.writerow(ROW)
        for row in data:
            print(row)
            writer.writerow(row)

def graf():
    data_DB = sns.load_dataset("test")
    data_DB.head()
    sns.scatterplot(data=data_DB, x="cpu_time", y="cpu_1")
    plt.show()


csv_w()
graf()