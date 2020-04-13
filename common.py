import datetime
import sys
import time
from gevent import thread


def IntervalTask(sec,func,args=()):
    def run():
        while 1:
            func(*args)
            time.sleep(sec)

    thread.start_new_thread(run, args)

def dbg_db(*args):
    res = '['+time_to_str(int(time.time()))+']----------process:'+str(sys.argv[-1]) + '\n'
    info = ''
    for i in args:
        info += '    '
        info += str(i)
        info += '\n'
    debug_info = res+info
    open('db.log','a').write(debug_info)
    return
    # print(*args)

def time_to_str(times=time.time()):
    if times == 0:
        return '2019-09-24 00:00:00'
    date_array = datetime.datetime.utcfromtimestamp(times + (8 * 3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")