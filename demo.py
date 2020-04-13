from dbservers.server import Data

# table_name = 'god'
table_name = 'shop_type'
# 查询1条 返回一个字典
# a = Data.find(table_name,[('id','=',1)])
# 查询多条，返回字典组成的列表
# b = Data.select(table_name,[('id','!=','0')])
# 更新数据 成功失败都返回None
# c = Data.update(table_name,[('id','=','14')],{'remark':'222'})
# 插入数据 成功返回None，失败返回失败原因
# d = Data.insert(table_name,[{'shop_id':613,'shop_type':3,'partner':0}])
# 删除数据，慎用
d = Data.delete(table_name,[('shop_id','=','613')])
# print(a)
# print(b)
# print(c)
print(d)
