from dbservers.server import Data


def create_table():
    Data.query('drop table TABLE_NAME1')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('Field1', 'int', 'default 0'),
        ('Field2', 'int', 'default 0'),
        ('Field3', 'int', 'default 0'),

    ]
    Data.create('TABLE_NAME1', colums)

create_table()
