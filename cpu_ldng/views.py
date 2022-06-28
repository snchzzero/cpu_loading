from django.shortcuts import render, redirect
from cpu_ldng.forms import Form_StartStop
from datetime import datetime
from celery import Celery  # для закрытия задачи по id
from .tasks import for_new_connection, start_script_insert_date, start_csv_create_figure

global name
name = 'home'
process_id_1 = ""
process_id_2 = ""


def time():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # получаем текущее время
    return(now)

def home(request):
    if request.method == 'GET':
        for_new_connection.delay()
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
            return render(request, 'cpu_ldng/home.html', {'form': Form_StartStop(), 'now': time(), 'name': name})


def start(request):
    global name
    name = "start"
    global process_id_1

    # удаляем задачу(процесс) по ее id
    celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
    celeryapp.control.revoke(process_id_1, terminate=True)
    process = start_script_insert_date.delay()
    process_id_1 = process.id

    return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def stop(request):
    global name
    name = "stop"
    try:
        # удаляем задачу(процесс) по ее id
        celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
        celeryapp.control.revoke(process_id_1, terminate=True)

        return render(request, 'cpu_ldng/home.html',
                      {'name': name, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def reset(request):
    global name
    name = "reset"
    try:
        # удаляем задачу(процесс) по ее id
        celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
        celeryapp.control.revoke(process_id_1, terminate=True)
        celeryapp.control.revoke(process_id_2, terminate=True)

        for_new_connection.delay()

        return render(request, 'cpu_ldng/home.html',
                      {'name': name, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def create_fig(request):
    global process_id_2
    process = start_csv_create_figure.delay()
    process_id_2 = process.id

    return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def send_fig(request):
    fig = "send_fig"
    try:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'fig': fig, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})