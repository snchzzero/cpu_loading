from cpu_loading.celory import app

from .script import start_script, new_connection
from .create_fig import csv_all, figure_1, csv_srez, figure_2

#считываем данные по процессору заносим в БД
@app.task   # оборачиваем в декоратор для отслеживания Celery
def start_script_insert_date():
    start_script()

#для формирования csv и построения графиков
@app.task
def start_csv_create_figure():
    csv_all()
    figure_1()
    csv_srez()
    figure_2()

#обнуляем БД
@app.task
def for_new_connection():
    new_connection()