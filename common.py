import base64
import datetime
import hashlib
import sys
import time
import xlwt
from gevent import thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 定时器
def IntervalTask(sec, func, args=()):
    def run():
        while 1:
            func(*args)
            time.sleep(sec)

    thread.start_new_thread(run, args)

# 日志管理
def dbg_db(*args):
    res = '[' + time_to_str(int(time.time())) + ']----------process:' + str(sys.argv[-1]) + '\n'
    info = ''
    for i in args:
        info += '    '
        info += str(i)
        info += '\n'
    debug_info = res + info
    open('db.log', 'a').write(debug_info)
    return
    # print(*args)

# 时间戳转字符串
def time_to_str(times=time.time()):
    if times == 0:
        return '2019-09-24 00:00:00'
    date_array = datetime.datetime.utcfromtimestamp(times + (8 * 3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")

# 处理表格数据
def make_excle_data(data):
    title = '标题1\t标题2\t标题3'
    title = title.split('\t')

    content_list = []

    if len(data) > 0:
        for i in data:
            content = str(i['字段1']) + '\t' + str(i['字段2']) + '\t' + str(i['字段3'])
            content = content.split('\t')
            content_list.append(content)

    result = {
        'colum': title,
        'content': content_list
    }
    write_excle(result, name='文档名称')


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

    file_name = name + str(time.time())
    f.save(file_name + '.xls')

    return file_name + '.xls'

# RSA 加密
def rsa_str(str):
    pub_key = ''
    pub = RSA.importKey(open(pub_key, 'rb').read())

    cryp = PKCS1_OAEP.new(pub)
    encrypted = cryp.encrypt(str.encode('utf-8'))

    res = base64.b64encode(encrypted)
    return res.decode('utf-8')

# md5
def get_md5(string):
    md5 = hashlib.md5(string.encode('ascii')).hexdigest()
    return md5
    # 计算md5校验
    # 这里python作为一个弱类型语言的坑就出现了
    # 竟然传入值需要解码成ascii
