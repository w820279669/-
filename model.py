from dbservers.server import Data


def take_record():
    Data.query('drop table TABLE_NAME1')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('字段1', 'int', 'default 0'),
        ('字段2', 'int', 'default 0'),
        ('字段3', 'int', 'default 0'),

    ]
    Data.create('TABLE_NAME1', colums)

