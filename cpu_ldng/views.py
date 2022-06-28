from django.shortcuts import render, redirect
import cpu_ldng.script
from cpu_ldng.script import new_connection
from cpu_ldng.forms import Form_StartStop
from datetime import datetime
from celery import Celery  # для закрытия задачи по id
from .tasks import start_script_insert_date

from celery.app.control import Control

from celery.worker.control import revoke


from .tasks import start_script_insert_date, start_csv_create_figure
from celery.app import default_app
from .create_fig import csv_all, csv_srez, figure_1, figure_2


#process_id = 0


def time():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # получаем текущее время
    return(now)

def home(request):
    if request.method == 'GET':
        new_connection()
        name = ""
        return render(request, 'cpu_ldng/home.html', {'form': Form_StartStop(), 'now': time(), 'name': name})
    elif request.method == 'POST':
        form = Form_StartStop(request.POST)
        if form.is_valid():
            start_f = form.cleaned_data.get("Start_Model")
            stop_f = form.cleaned_data.get("Stop_Model")
            reset_f = form.cleaned_data.get("Reset_Model")
            create_fig_f = form.cleaned_data.get("Create_Fig_Model")
            send_fig_f = form.cleaned_data.get("Send_Fig_Model")
        else:
            start_f = ("NOstart")
            stop_f = ("NOstop")
            reset_f = ("NOreset")
            create_fig_f = ("NOcreate_fig")
            send_fig_f = ("NOsend_fig")

        if start_f == "start":
            return redirect('start')
        elif stop_f == "stop":
            return redirect('stop')
        elif reset_f == "reset":
            return redirect('reset')
        elif create_fig_f == "create_fig":
            return redirect('create_fig')
        elif send_fig_f == "send_fig":
            return redirect('send_fig')
        else:
            name = ""
            return render(request, 'cpu_ldng/home.html', {'form': Form_StartStop(), 'now': time(), 'name': name})


def start(request):
    name = "start"
    global process_id
    process = start_script_insert_date.delay()
    process_id = process.id

    # process = start_script_insert_date.delay()  # delay запускает функцию в фоне
    # global process_id
    # process_id = process.id

    return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def stop(request):
    name = "stop"
    try:
        # удаляем задачу(процесс) по ее id
        celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
        celeryapp.control.revoke(process_id, terminate=True)
        #process_id = 0
        return render(request, 'cpu_ldng/home.html',
                      {'name': name, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})

def reset(request):
    name = "reset"
    try:
        # удаляем задачу(процесс) по ее id
        celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
        celeryapp.control.revoke(process_id, terminate=True)
        new_connection()
        return render(request, 'cpu_ldng/home.html',
                      {'name': name, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def create_fig(request):
    #test_txt()
    start_csv_create_figure.delay()
    #csv_all()
    #figure_1()
    #csv_srez()
    #figure_2()

    # process = start_script_insert_date.delay()  # delay запускает функцию в фоне
    # global process_id
    # process_id = process.id

    return render(request, 'cpu_ldng/home.html', {'now': time()})

def send_fig(request):
    fig = "send_fig"
    try:

        return render(request, 'cpu_ldng/home.html',{'fig': fig, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'now': time()})