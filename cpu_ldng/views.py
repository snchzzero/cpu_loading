from django.shortcuts import render, redirect
import cpu_ldng.script
from cpu_ldng.script import new_connection
from cpu_ldng.forms import Form_StartStop
from datetime import datetime
from celery import Celery
from .tasks import start_script_insert_date

from celery.app.control import Control

from celery.worker.control import revoke


from .tasks import start_script_insert_date
from celery.app import default_app



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
        else:
            start_f = "ничего старт"
            stop_f = "ничего стоп"
        if start_f == "start":
            return redirect('start')
        elif stop_f == "stop":
            return redirect('stop')
        else:
            name = ""
            return render(request, 'cpu_ldng/home.html', {'form': Form_StartStop(), 'now': time(), 'name': name})




def start(request):
    name = "start"
    global process_id, process
    process = start_script_insert_date.delay()
    process_id = process.id

    # process = start_script_insert_date.delay()  # delay запускает функцию в фоне
    # global process_id
    # process_id = process.id

    #loop.run_until_complete(start_script())
    # new_connection()
    # loop_remote(True)
    #asyncio.ensure_future(start_script())
    #loop.run_forever()
    return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def stop(request):
    name = "stop"
    try:


        # loop_remote(False)
        #stop_script(False)
        #celery_app.control.revoke(process_id, terminate=True)
        #control.revoke(process_id)
        #Control.revoke(self=() ,task_id=process_id)

        #default_app.control.revoke(process_id, terminated=True, signal='SIGKILL')

        #start_script_insert_date.control.revoke(process_id, terminate=True) # не рабочий вар

        # удаляем задачу(процесс) по ее id
        celeryapp = Celery('app', broker="redis://app_redis:6379/0", backend="redis_uri")
        celeryapp.control.revoke(process_id, terminate=True)

        #celery.app.control.Control.revoke(task_id=process_id, terminate=True)
        #Control.revoke(task_id=process_id, terminate=True)

        #celery.app.control.Control(process_id, terminate=True)
        #app.control.revoke(process_id, terminate=True)
        return render(request, 'cpu_ldng/home.html', {'name': process_id, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})




