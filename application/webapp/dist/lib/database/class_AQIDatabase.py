# coding=UTF-8

#-----------------------------------------------
# class_AQIDatabase文件
# @class: AQIDatabase类
# @introduction:AQIDatabase类连接AQI数据库集合进行操作
# @dependency: Database
# @author: plutoese
# @date: 2016.01.05
#------------------------------------------------
"""
.. code-block:: python

    db = CEICDatabase()
    period = db.period
"""

import re
import pandas as pd
import numpy as np
from webapp.dist.lib.database.class_regionformat import RegionFormat
from pymongo import ASCENDING
from webapp.dist.lib.database.class_Database import Database

class AQIDatabase(Database):
    """ AQIDatabase类连接AQI数据库集合进行操作
    """
    def __init__(self):
        Database.__init__(self)
        self.connect('internetDB', 'AQI')

    # 查询
    def find(self,conds,toStandardForm=True):

        print(conds)
        # 设置projection
        projection = {'city':1,'AQI指数':1,'日期':1,'No2':1,'_id':0,'Co':1,
                          '当天AQI排名':1,'PM25':1,'So2':1,'质量等级':1,'PM10':1}

        # 设置sorts
        sorts= [('日期',ASCENDING),('city',ASCENDING)]

        # 设置时间
        start_date = conds.get('sdate')
        end_date = conds.get('edate')

        # 设置区域
        region = conds.get('region')

        result = []
        conditions = dict()
        conditions['city'] = {'$in': region}
        conditions['日期'] = {'$gte': start_date,'$lte': end_date}
        mresult = pd.DataFrame(list(self.collection.find(conditions,projection).sort(sorts)))

        if mresult is None:
            return None

        if len(mresult.values) < 1:
            return None

        mresult = mresult.drop_duplicates(keep='last')

        result = []
        cols = ['日期','city', 'AQI指数','PM10','PM25','Co','No2','So2','当天AQI排名','质量等级']
        for key in mresult['日期'].index:
            result.append([mresult[col][key] for col in cols])
        return {'header':cols,'data':result}

    @property
    def period(self):
        return sorted(self.collection.find().distinct('日期'))

    @property
    def city(self):
        return sorted(self.collection.find().distinct('city'))


if __name__ == '__main__':
    db = AQIDatabase()
    print(db.collection)
    print(db.period)
    print(db.city)

    conds = {'region':['上海', '东莞'],'sdate':'2015-08-01','edate':'2016-01-02'}
    mdata = db.find(conds)
    print('-----------------------------')
    print(mdata['header'])
    print(mdata['data'])


