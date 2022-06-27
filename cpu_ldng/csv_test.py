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
    data = pd.read_csv('test.csv')
    data.head()
    #print(data)
    #data_DB = sns.get_data_home('test')

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

    #sns.barplot(x="cpu_time", y="cpu_1", data=data)
    #sns.displot(data=data, x="cpu_time", kind="hist")

    #sns.catplot(x="cpu_time", y="cpu_1", kind="bar", data=data, palette="pastel")

    # for cpu_id in range(1, cpu_col + 1):
    #     swarm_plot = sns.lineplot(x="cpu_time", y=f"cpu_{cpu_id}", ci=None, data=data)
    #
    # swarm_plot.figure.savefig("output.png")
    #plt.show()



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



csv_w()
graf()