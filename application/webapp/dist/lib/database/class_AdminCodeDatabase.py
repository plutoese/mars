# coding=UTF-8

#-----------------------------------------------
# class_AdminDatabase文件
# @class: AdminDatabase类
# @introduction: AdminDatabase类用来处理区域行政区划
# @dependency: pymongo，Database类
# @author: plutoese
# @date: 2015.10.17
#------------------------------------------------

'''
.. code-block:: python

    db = AdminDatabase()
    print(db.collection)
    print(db.period)
    print(db.version(year=2004))
    print(db.find())
    print(list(db.find(year='2010',projection={'region':1,'_id':0})))
    print(list(db.find(adminlevel=2,version='2004_12_31')))
'''
from lib.database.class_Database import Database
from pymongo import ASCENDING


class AdminCodeDatabase(Database):
    '''AdminDatabase类用来处理区域行政区划

    '''

    def __init__(self):
        Database.__init__(self)
        self.connect('regionDB', 'AdminCode')

    def find(self, **conds):
        '''查询AdminCode数据库集合

        :param dict conds: 查询参数集合，其中包括查询条件condition，映射projection，排序sorts
        :return: 查询结果
        :rtype: pymongo.cursor.Cursor对象
        '''
        # 设置projection
        projection = conds.get('projection')
        if projection is None:
            projection = {'region': 1, 'version': 1,
                          'adminlevel': 1, 'acode': 1, '_id': 1, 'parent': 1}
        else:
            conds.pop('projection')
        # 设置sorts
        sorts = conds.get('sorts')
        if sorts is None:
            sorts = [('year', ASCENDING), ('acode', ASCENDING)]
        else:
            conds.pop('sorts')

        # 设置查询条件
        condition = dict()
        for key in conds:
            if isinstance(conds[key], list):
                condition[key] = {'$in': conds[key]}
            else:
                condition[key] = conds[key]

        # 返回查询结果
        return self.collection.find(condition, projection).sort(sorts)

    @property
    def period(self):
        '''数据集合AdminCode中的时间跨度

        :return: 数据集合AdminCode中所有年份
        :rtype: list
        '''
        return sorted(self.find().distinct('year'))

    def version(self, year=None):
        '''版本号

        :param int,str year: 年份
        :return: 数据集合中所有版本号或者某一年的版本号
        :rtype: list
        '''
        if year is None:
            return sorted(self.find().distinct('version'))
        else:
            return sorted(self.find(year=str(year)).distinct('version'))

if __name__ == '__main__':
    db = AdminCodeDatabase()
    print(db.collection)
    print(db.period)
    print(db.version(year=2005))
    print(db.find())
    print(list(db.find(year='2010', projection={'region': 1, '_id': 0})))
    print(list(db.find(adminlevel=2, version='2004_12_31')))
