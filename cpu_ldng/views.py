from django.shortcuts import render, redirect
from cpu_ldng.script import new_connection, start_script, stop, loop_remote
from cpu_ldng.forms import Form_StartStop
from cpu_ldng.models import ModelStartStop
from datetime import datetime
import asyncio
import nest_asyncio
nest_asyncio.apply()

# loop = asyncio.get_event_loop()


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
    #loop.run_until_complete(start_script())

    loop_remote(True)
    #asyncio.ensure_future(start_script())
    #loop.run_forever()
    return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})


def stop(request):
    name = "stop"
    try:
        loop_remote(False)
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})
    except ValueError:
        return render(request, 'cpu_ldng/home.html', {'name': name, 'now': time()})
    #loop.close()
    #loop.is_closed()
    #loop.shutdown_asyncgens(start_script)
    #stop(False)




