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
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        data = select_all()
        ROW =  ['cpu_5sec_id', 'cpu_time']
        for i in range(1, int(cpu_col) + 1):
            ROW.append(f'cpu_{i}')
        writer.writerow(ROW)
        for row in data:
            print(row)
            writer.writerow(row)

def figure_1():
    data = pd.read_csv('test.csv')
    data.head()

    sns.set(font_scale=0.7)  # размер надписей к осям
    plt.figure(figsize=(10, 15))
    for cpu_id in range(1, cpu_col + 1):
        swarm_plot = sns.lineplot(data=data, x='cpu_time', y=f'cpu_{cpu_id}', legend=False)
    plt.legend(labels=[f"ядро{cpu_id}" for cpu_id in range(1, cpu_col + 1)], loc='upper right')  # добавляем легенду
    swarm_plot.set_title("История измения моментальной загрузки процессора")
    swarm_plot.set_ylabel("загрузка процессора")
    swarm_plot.set_xlabel("время, шаг(5сек.)")
    plt.xticks(rotation=90)
    swarm_plot.figure.savefig("output_1.png")
    plt.show()

    # cpu_1 = list(data.iloc[:,2])
    # cpu_2 = list(data.iloc[:,3])
    # cpu_3 = list(data.iloc[:,4])
    # cpu_4 = list(data.iloc[:,5])

    # столбчатый график, требует настройки
    # data = pd.read_csv('test.csv')
    # data.head()
    # time = data.iloc[:,1]
    #index = list(time)
    #fig = plt.axis([0, 30, 0, 8])  # размеры полотна
    #plt.title('A Multiseries Bar Chart', fontsize=20)
    # color = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'black',
    #          'gold', 'lime', 'indigo', 'coral', 'chocolate', 'magenta']
    # xplot = 0
    # for cpu_id in range(1, cpu_col + 1):
    #     plt.bar([ox + xplot for ox in range(len(index))],
    #             [cpu for cpu in list(data.iloc[:, cpu_id + 1])],
    #             color=color[cpu_id-1],
    #             label=f"ядро{cpu_id}",
    #             width=0.3
    #
    #     )
    #     xplot += 0.4
    #
    # plt.xticks(range(len(index)), index)
    # fig.autofmt_xdate(rotation=45)
    # plt.show()
    # plt.legend(loc="upper right")
    # plt.savefig("График.png")


def csv_srez():



    # записываем среднее значение по всем ядрам за каждые 5 сек
    with open('srez_1.csv', 'w') as f:
        data = pd.read_csv('test.csv')
        writer = csv.writer(f)
        ROW =  ['cpu_5sec_id', 'cpu_time', 'cpu_avg']
        writer.writerow(ROW)
        for id in data['cpu_5sec_id']:
            row_1 = list(data.iloc[id-1, :2])
            row_2 = round((sum(list(data.iloc[id-1, 2:])) / cpu_col), 2)  # средняя нагрузка на все ядра за 5 сек
            row_1.append(row_2)
            writer.writerow(row_1)
    # записываем среднее значение по среднему ядру за 1мин (60/5=12)
    with open('srez_2.csv', 'w') as f:
        data = pd.read_csv('srez_1.csv')
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

def figure_2():
    pass



csv_all()
figure_1()
csv_srez()
#figure_2()