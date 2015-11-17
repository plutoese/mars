# coding=UTF-8

#-----------------------------------------------
# class_Database文件
# @class: Database类
# @introduction:Database类连接MongoDB数据库进行操作
# @dependency: pymongo
# @author: plutoese
# @date: 2015.10.17
#------------------------------------------------
'''
.. code-block:: python

    db = MongoDB()
    db.connect('regionDB','CEIC')
'''

from pymongo import MongoClient,ASCENDING,IndexModel

class Database:
    ''' Database类连接MongoDB数据库进行操作

    :param str host: 数据库主机，默认是'localhost'
    :param int port: 数据库端口，默认是27017
    :return: 无返回值
    '''

    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host, port)

    def connect(self, database_name, collection_name):
        '''连接MongoDB数据中的集合

        :param str database_name: 数据库名称
        :param str collection_name: 集合名称
        :return: 数据集合的连接
        :rtype: pymongo.collection.Collection对象
        '''
        if database_name in self.client.database_names():
            self.db = self.client[database_name]
        else:
            print('No such database: ', database_name)
            raise NameError
        if collection_name in self.db.collection_names():
            self.collection = self.db[collection_name]
        else:
            print('No such collection: ', collection_name)
            raise NameError
        return self.collection

    def insert(self,record):
        '''插入数据到Mongodb数据库中的集合

        :param dict,list record: 数据记录
        :return: 无返回值
        '''
        self.collection.insert(record)

    def create_index(self,indexes):
        '''建立索引

        :param IndexModel indexes: 索引条目
        :return: 无返回值
        '''
        self.collection.create_indexes(indexes)


if __name__ == '__main__':
    db = Database()
    print(db.client.database_names())
    con = db.connect('regionDB', 'CEIC')
    print(con)
