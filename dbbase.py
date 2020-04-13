import time
import pymysql

from dbservers import dbconfig
from dbservers.common import IntervalTask, dbg_db


class Base(object):

    def __init__(self, host, user, psw, dbname):
        self._host = host
        self._user = user
        self._psw = psw
        self._dbname = dbname
        self._tables = {}
        self._is_busy = 0
        self.init_time = int(time.time())
        self.executing_query = ''
        self.last_execute_time = int(time.time())
        self.db = None
        self.connect_db()
        self.last_connect_time = int(time.time())

    def connect_db(self):
        try:
            self.db = pymysql.connect(self._host, self._user, self._psw, self._dbname, charset='utf8', autocommit=True)
            self._load_tables()
            print('数据库模块连接成功')
            dbg_db('数据库模块连接成功')
            # IntervalTask(30, self.keep_connect)
        except Exception as e:
            print(e)
            print('数据库没有成功链接')
            dbg_db('数据库模块连接成功', str(e))
            pass

    def become_busy(self):
        self._is_busy = 1
        return

    def become_free(self):
        self._is_busy = 0
        return

    def is_busy(self):
        if self._is_busy == 1:
            return True
        else:
            return False

    def keep_connect(self):
        if self.db == None:
            self.connect_db()

        # print(id(self),'进行连接')
        self.query('select 1')
        # print('数据库心跳')

    def connect(self):
        self.db = pymysql.connect(self._host, self._user, self._psw, self._dbname, charset='utf8')

    def load_an_table(self, table):
        sql = 'show fields from ' + table
        res = self.query(sql)
        self._tables[table] = list(map(lambda x: x[0], res))
        return

    # 加载所有数据库表名
    def _load_tables(self):
        sql = 'show tables'
        res = self.query(sql)
        tables = tuple(map(lambda x: x[0], res))
        # print(tables)
        for table in tables:
            sql = 'show fields from ' + table
            #
            res = self.query(sql)
            self._tables[table] = list(map(lambda x: x[0], res))

    def _load_all_fileds(self):
        pass

    def create(self, table, colums):
        sql = 'create table %s(' % table

        tail = ''
        for item in colums:
            col = ''
            for i in item:
                col += str(i)
                col += ' '
            col += ','
            tail += col

        tail = tail[:-1] + ')'
        sql += tail

        #

        self.query(sql)
        self.db.commit()
        return

    # 查找数据（单条）
    def find(self, table, conditions, fields='*', order=None):
        sql = 'select %s from %s where  ' % (fields, table)
        # if conditions == []:
        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + "  and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        if order is not None:
            sql += 'order by %s %s ' % (order[0], order[1])

        sql += " limit 1"

        #
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if '*' == fields:
            fieldList = self._tables[table]

        else:
            fieldList = fields.split(',')

        self.db.commit()
        return dict(zip(fieldList, res[0]))

    # 查找数据
    def select(self, table, conditions, fields='*', order=None):
        sql = 'select %s from %s where  ' % (fields, table)

        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + "  and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        if order is not None:
            sql += 'order by %s %s ' % (order[0], order[1])

        #
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if '*' == fields:
            fieldList = self._tables[table]
        else:
            fieldList = fields.split(',')

        result = []
        for data in res:
            data = dict(zip(fieldList, data))
            result.append(data)

        self.db.commit()
        return result

    def insert(self, table, content, isCommit=True):
        if type(content) == type([]):
            sql = ''
            for params in content:
                keys = str(tuple(params.keys()))
                keys = keys.replace("'", "")
                values = str(tuple(params.values()))
                if (1 == len(params)):
                    keys = keys[:-2] + ")"
                    values = values[:-2] + ")"

                sql += 'insert into %s%s values %s ;' % (table, keys, values)
            #
            self.query(sql)
            if True == isCommit:
                self.db.commit()
        else:
            params = content
            keys = str(tuple(params.keys()))
            keys = keys.replace("'", "")
            values = str(tuple(params.values()))
            if (1 == len(params)):
                keys = keys[:-2] + ")"
                values = values[:-2] + ")"

            sql = 'insert into %s%s values %s ;' % (table, keys, values)
            #
            self.query(sql)
            if True == isCommit:
                self.db.commit()

        return

    def update(self, table, conditions, params, isCommit=True):
        sql = 'update %s set ' % table
        for param, value in params.items():
            if type("") == type(value):
                value = "'%s'" % value
            sql = sql + " %s = %s," % (param, value)

        sql = sql[:-1]
        if len(conditions) > 0:
            sql += " where "

        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(conditions):
            sql = sql[0: -4]

        #
        self.query(sql)
        if True == isCommit:
            self.db.commit()

        return

    def delete(self, table, condition, is_commit):
        sql = 'delete from %s where ' % table
        for unit in condition:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(condition):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]
        #
        #
        self.query(sql)
        if is_commit is True:
            self.db.commit()

        return

    def query(self, sql):

        self.executing_query = sql

        if sql != 'select 1':
            if dbconfig.show_sql == True:
                print(sql)
        try:
            self.db.ping(reconnect=True)
        except Exception as e:
            print(sql, '数据库连接出错', str(e), '进行重连')
            dbg_db(sql, '数据库连接出错', str(e), '进行重连')
            self.connect()
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            self.update_last_execute_time()
            self.db.commit()
            # dbg_db(sql,'数据库查询成功')
        except Exception as e:
            print('<--------DBERROR-------->')
            print(sql)
            print('数据库查询出错', str(e))
            print('<--------DBERROR-------->')
            dbg_db(sql, '数据库查询出错', str(e))
            results = None

        self.update_last_connect_time()

        self.executing_query = ''

        return results
        # results = cursor.fetchall()

    def update_last_connect_time(self):
        self.last_connect_time = int(time.time())
        return

    def update_last_execute_time(self):
        self.last_execute_time = int(time.time())
        return

    def get_last_connect_time(self):
        return self.last_connect_time

    def query_one(self, sql):
        self.db.ping(reconnect=True)
        # cur.execute(sql)
        # dbservers.commit()
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

    def truncate(self, table):
        sql = 'TRUNCATE TABLE %s' % table
        self.query(sql)

        return

    def find_last(self, table, conditions, order_column, quantity, fields="*"):

        sql = 'select %s from %s where  ' % (fields, table)
        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + "  and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        sql += 'order by %s DESC limit %s' % (order_column, quantity)

        #
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if '*' == fields:

            fieldList = self._tables[table]
        else:
            fieldList = fields.split(',')

        # else:
        #     fieldList = str.split(fields)

        self.db.commit()
        return dict(zip(fieldList, res[0]))


class data_manager(object):
    def __init__(self,db_config):
        self.t_data = db_config
        self.sql_pool = {}

        sql = self.create_new_sql()
        self.add_new_sql(sql)
        print('创建首批数据库链接实例')
        IntervalTask(10,self.keep_connect)

    # def kill_hanged_connection(self):
    #     dead_sql = []
    #

    def keep_connect(self):
        can_update_sql = []
        for sql in self.sql_pool.values():
            if int(time.time())-sql.get_last_connect_time()  > 30:
                can_update_sql.append(sql)

        for sql in can_update_sql:
            if sql.is_busy() == False:
                sql.become_busy()
                sql.keep_connect()
                sql.become_free()
        return

    def find_free_sql(self):
        for sql in self.sql_pool.values():
            if sql.is_busy() == False:
                sql.become_busy()
                return sql
        print('数据库连接池全忙状态，创建新的数据库链接')
        sql = self.create_new_sql()
        sql.become_busy()
        self.add_new_sql(sql)
        print('创建完毕')
        dbg_db('数据库连接池全忙状态，创建新的数据库链接', '新连接id:', id(sql))
        return sql

    def add_new_sql(self,sql):
        self.sql_pool[id(sql)] = sql
        return


    def create_new_sql(self):
        sql = Base(self.t_data['host'], self.t_data['user'], self.t_data['password'], self.t_data['database'])
        # sql.become_busy()
        # self.sql_pool.append(sql)
        return sql


    def get_tables(self):
        sql = self.find_free_sql()
        # sql.become_busy()
        print('执行这次sql请求的链接是', id(sql))
        result = sql._tables
        sql.become_free()
        return result


    def create(self,table, colums):
        sql = self.find_free_sql()
        # sql.become_busy()
        print('执行这次sql请求的链接是', id(sql))
        result = sql.create(table, colums)
        sql.become_free()
        return result


    def insert(self,table, params, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.insert(table, params, is_commit)
        sql.become_free()
        return result


    def find(self,table, conditions, fields='*', order=None):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.find(table, conditions, fields, order)
        sql.become_free()
        return result


    def select(self,table, conditions, fields='*', order=None):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.select(table, conditions, fields, order)
        sql.become_free()
        return result


    def update(self,table, conditions, params, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.update(table, conditions, params, is_commit)
        sql.become_free()
        # print(sql.become_free())
        return result


    def delete(self,table, conditions, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.delete(table, conditions, is_commit)
        sql.become_free()
        return result


    def find_last(self,table, conditions, info, limit):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.find_last(table, conditions, info, limit)
        sql.become_free()
        return result




    def query(self,sql_query):
        # print(sql)
        sql = self.find_free_sql()
        # sql.become_busy()
        print('执行这次sql请求的链接是', id(sql))
        result = sql.query(sql_query)
        sql.become_free()
        return result

    # @staticmethod
    # def truncate(table):
    #     # print(sql)
    #     return Data.sql.truncate(table)
