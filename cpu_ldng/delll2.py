def start():
    save(56, 2022)

def save(last_id, last_time):
    global lastid, lasttime
    lastid, lasttime = last_id, last_time

def stop_time_id():
    return lastid, lasttime