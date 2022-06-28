from cpu_loading.celory import app

from .script import start_script
from .create_fig import csv_all, figure_1, csv_srez, figure_2


@app.task   # оборачиваем в декоратор для отслеживания Celery
def start_script_insert_date():
    start_script()

@app.task
def start_csv_create_figure():
    csv_all()
    figure_1()
    csv_srez()
    figure_2()