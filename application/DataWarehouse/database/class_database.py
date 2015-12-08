# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: Database
# @introduction: 类Database表示数据库，是超类，用来被继承。
# @property:
# - collection: 数据库接口
# @method:
# - _connect(db,collection)：连接相应的数据库，参数db是数据库名称，字符串；collection是集合
#                           名称，字符串。无返回值。
# -----------------------------------------------------------------------------------------

from pymongo import MongoClient

class Database:
    '''
    类Database用来连接数据库
    '''

    # 属性
    # 连接数据库参数设置
    Host = 'localhost'
    Port = 27017

    # 构造函数
    def __init__(self):
        self.client = MongoClient(self.Host,self.Port)

    # 连接数据库集合
    def _connect(self, db=None, collection=None):
        self.db = self.client[db]
        self.collection = self.db[collection]

if __name__ == '__main__':
    db = Database()
    db._connect('regionDB','CityStatistics')


















