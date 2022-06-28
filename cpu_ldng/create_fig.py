from cpu_ldng.config_db import host, user, password, db_name, port
import psycopg2
import psutil
import csv
from django.conf import settings

#графики
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


cpu_col = psutil.cpu_count()  # кол-во ядер

def select_all():
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

def csv_all():
    with open('/usr/src/cpu_loading/cpu_ldng/csv_all.csv', 'w') as f:
        writer = csv.writer(f)
        data = select_all()
        ROW =  ['cpu_5sec_id', 'cpu_time']
        for i in range(1, int(cpu_col) + 1):
            ROW.append(f'cpu_{i}')
        writer.writerow(ROW)
        for row in data:
            print(row)
            writer.writerow(row)
        print("csv_all успешно")

def figure_1():
    data = pd.read_csv('/usr/src/cpu_loading/cpu_ldng/csv_all.csv')
    data.head()

    sns.set(font_scale=1.3)  # размер надписей к осям
    plt.figure(figsize=(22, 10))
    for cpu_id in range(1, cpu_col + 1):
        swarm_plot = sns.lineplot(data=data, x='cpu_time', y=f'cpu_{cpu_id}', legend=False)
    plt.legend(labels=[f"ядро{cpu_id}" for cpu_id in range(1, cpu_col + 1)], loc='upper right')  # добавляем легенду
    swarm_plot.set_title("История изменения моментальной загрузки процессора в течении последнего часа")
    swarm_plot.set_ylabel("загрузка процессора")
    swarm_plot.set_xlabel("время, шаг(5сек.)")
    plt.xticks(color='w')
    #plt.xticks(rotation=90)
    swarm_plot.figure.savefig("/usr/src/cpu_loading/cpu_ldng/static/cpu_ldng/output_1.png")
    print("рисунок 2 успешно")
    #plt.show()

def csv_srez():

    # записываем среднее значение по всем ядрам за каждые 5 сек
    with open('/usr/src/cpu_loading/cpu_ldng/srez_1.csv', 'w') as f:
        data = pd.read_csv('/usr/src/cpu_loading/cpu_ldng/csv_all.csv')
        writer = csv.writer(f)
        ROW =  ['cpu_5sec_id', 'cpu_time', 'cpu_avg']
        writer.writerow(ROW)
        for id in data['cpu_5sec_id']:
            row_1 = list(data.iloc[id-1, :2])
            row_2 = round((sum(list(data.iloc[id-1, 2:])) / cpu_col), 2)  # средняя нагрузка на все ядра за 5 сек
            row_1.append(row_2)
            writer.writerow(row_1)

    # записываем среднее значение по всему процессору за 1мин (60/5=12)
    with open('/usr/src/cpu_loading/cpu_ldng/srez_2.csv', 'w') as f:
        data = pd.read_csv('/usr/src/cpu_loading/cpu_ldng/srez_1.csv')
        writer = csv.writer(f)
        ROW = ['cpu_5sec_id', 'cpu_time', 'cpu_avg']
        writer.writerow(ROW)
        len_max = len(data['cpu_5sec_id'])

        for id in range(0, len_max, 12):
            if id + 12 >= len_max:
                row_2 = round((sum(list(data.iloc[id :, 2])) / 12), 2)
            else:
                row_2 = round((sum(list(data.iloc[id : (id + 12), 2])) / 12), 2)
            row_1 = list(data.iloc[id , 0:2])
            row_1.append(row_2)
            writer.writerow(row_1)

        print("csv_срез успешно успешно")

def figure_2():
    data = pd.read_csv('/usr/src/cpu_loading/cpu_ldng/srez_2.csv')
    data.head()

    sns.set(font_scale=1.2)  # размер надписей к осям
    plt.figure(figsize=(22, 10))

    swarm_plot = sns.lineplot(data=data, x='cpu_time', y='cpu_avg', legend=False)

    #plt.legend(labels='cpu', loc='upper right')  # добавляем легенду

    swarm_plot.set_title("Усредненная загрузка процессора в течении последнего часа")
    swarm_plot.set_ylabel("загрузка процессора")
    swarm_plot.set_xlabel("время, шаг(60сек.)")
    plt.xticks(rotation=90)
    swarm_plot.figure.savefig("/usr/src/cpu_loading/cpu_ldng/static/cpu_ldng/output_2.png")
    print("рисунок 2 успешно")
    #plt.show()


# csv_all()
# figure_1()
# csv_srez()
# figure_2()
