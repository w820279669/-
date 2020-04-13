import datetime
import hashlib
import random
import string
import sys
import time

import xlwt
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


def make_excle_data(data):
    title = '角色\t姓名\t电话'
    title = title.split('\t')

    content_list = []

    if len(data) > 0:
        for i in data:
            content = str(i['role']) + '\t' + i['name'] + '\t' + str(i['phone'])
            content = content.split('\t')
            content_list.append(content)

    result = {
        'colum': title,
        'content': content_list
    }
    write_excle(result, name='文档')


def write_excle(data={}, name=''):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet_1', cell_overwrite_ok=True)
    colum_title = data['colum']
    # 写第一行
    for i in range(0, len(colum_title)):
        sheet1.write(0, i, colum_title[i])

    content = data['content']
    count = 0
    for line in content:
        if len(line) == len(data['colum']):
            count += 1
            for i in range(0, len(line)):
                sheet1.write(count, i, str(line[i]))
        else:
            continue

    file_name = name +  str(time.time())
    f.save(file_name + '.xls')

    return file_name + '.xls'

# 相反
def create_rand_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

def get_md5(string):
    md5 = hashlib.md5(string.encode('ascii')).hexdigest()
    return md5
    # 计算md5校验
    # 这里python作为一个弱类型语言的坑就出现了
    # 竟然传入值需要解码成ascii