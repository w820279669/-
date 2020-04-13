from dbservers.server import Data

table_name = ''
# 查询1条 返回一个字典
check_params = ('key1','=','value1')
a = Data.find(table_name,[check_params])

# 查询多条，返回字典组成的列表
b = Data.select(table_name,[check_params])

# 更新数据 成功失败都返回None
update_params={
    'key2':'value2'
}
c = Data.update(table_name,[check_params],update_params)

# 插入数据 成功返回None，失败返回失败原因
insert_params1 = {
    'key1':'value1',
    'key2':'value2',
}
insert_params2 = {
    'key1':'value3',
    'key2':'value4',
}
d = Data.insert(table_name,[insert_params1,insert_params2])

# 删除数据，慎用
del_params =  ('key2','=','value2')
e = Data.delete(table_name,[del_params])

# print(a)
# print(b)
# print(c)
# print(d)
# print(e)
