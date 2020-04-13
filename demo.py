from dbservers.server import Data

table_name = ''
# 查询1条 返回一个字典
a = Data.find(table_name,[('id','=','1')])
# 查询多条，返回字典组成的列表
b = Data.select(table_name,[('id','!=','0')])
# 更新数据 成功失败都返回None
params1={
    '字段2':'value2'
}
c = Data.update(table_name,[('字段1','=','value1')],params1)
# 插入数据 成功返回None，失败返回失败原因
params2 = {
    '字段1':'value1',
    '字段2':'value2',
}
params3 = {
    '字段1':'value1',
    '字段2':'value2',
}
d = Data.insert(table_name,[params2,params3])
# 删除数据，慎用
e = Data.delete(table_name,[('字段','=','value')])
# print(a)
# print(b)
# print(c)
# print(d)
# print(e)
