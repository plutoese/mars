# coding=UTF-8

#-----------------------------------------------
# class_CEICDatabase文件
# @class: CEICDatabase类
# @introduction:CEICDatabase类连接CEIC数据库集合进行操作
# @dependency: pymongo
# @author: plutoese
# @date: 2016.01.03
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

class CEICDatabase(Database):
    """ CEICDatabase类连接CEIC数据库集合库进行操作
    """
    def __init__(self):
        Database.__init__(self)
        self.connect('regionDB', 'CEIC')

    def get_region_by_year(self,year):
        """ 获得某年的可选择的区域

        :param int year: 年份
        :return: 区域字典
        :rtype: dict
        """
        region_acode = sorted(self.collection.find({'year':year}).distinct('acode'))
        region_recode = [self.collection.find_one({'year':year,'acode':acode}) for acode in region_acode]
        region_dict = {item['acode']:item['region'] for item in region_recode}
        return region_dict

    def get_variables_from_period_regions(self,period,regions):
        period = [int(p) for p in period]
        regions = sorted(regions)
        if '000000' in regions:
            regions.pop(0)
        var = self.collection.find({'year':{'$in':period},'acode':{'$in':regions}}).distinct('variable')

        variables = [{"type": "option", "value": v, "label": v} for v in var]
        return variables

    # 查询
    def find(self,conds,toStandardForm=True):

        print(conds)
        # 设置projection
        projection = conds.get('projection')
        if projection is None:
            projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'unit':1}
        else:
            conds.pop('projection')
        # 设置sorts
        sorts = conds.get('sorts')
        if sorts is None:
            sorts= [('year',ASCENDING),('acode',ASCENDING)]
        else:
            conds.pop('sorts')

        # 设置时间
        period = conds.get('year')
        if period is None:
            variables = conds.get('variable',self.variables)
            period = self.period(variables)
        else:
            period = [int(y) for y in period]
            conds.pop('year')

        result = []
        conditions = dict()
        for key in conds:
            if re.match('region',key) is not None:
                continue
            if isinstance(conds[key],list):
                conditions[key] = {'$in':conds[key]}
            else:
                conditions[key] = conds[key]

        # 重点是设置区域
        if 'region' in conds:
            for year in period:
                conditions['year'] = year
                conditions['acode'] = {'$in': conds['region']}
                result.extend(list(self.collection.find(conditions,projection).sort(sorts)))
            mresult = pd.DataFrame(result)
        else:
            if isinstance(period,list):
                conditions['year'] = {'$in':period}
            else:
                conditions['year'] = period
            mresult = pd.DataFrame(list(self.collection.find(conditions,projection).sort(sorts)))

        if mresult is None:
            return None

        mresult = mresult.drop_duplicates(keep='last')
        cols = mresult.columns.tolist()
        print(cols)
        var_unit_dict = dict(zip(mresult.variable,mresult.unit))
        mresult.columns = pd.Index(cols)
        if toStandardForm:
            rformat = RegionFormat(mresult)
            my_result = rformat.transform()
            my_data = my_result['data']

            main_columns = []
            for item in my_data.columns.tolist():
                if var_unit_dict.get(item) is None:
                    main_columns.append(item)
                else:
                    main_columns.append('('.join([item,var_unit_dict.get(item)])+')')
            print(main_columns)
            if 'region' in main_columns:
                main_columns[main_columns.index('region')] = u'区域'
            if 'sdata' in my_result.keys():
                columns = ['时间']
                columns.extend(main_columns)
            elif 'pdata' in my_result.keys():
                columns = ['时间','区域代码']
                columns.extend(main_columns)
            else:
                columns = ['区域代码']
                columns.extend(main_columns)

            table_data = []
            my_data = my_data.dropna(how='all')
            my_data = my_data.fillna('')
            for i in range(len(my_data.index.tolist())):
                tmp_record = my_data.index.tolist()[i]
                if isinstance(tmp_record,tuple):
                    tmp_record = list(tmp_record)
                else:
                    tmp_record = [tmp_record]
                tmp_record.extend(my_data.values[i])
                table_data.append(tmp_record)
            print(columns)
            print(table_data)
            return {'header':columns,'data':table_data}
        else:
            return mresult

    @property
    def period(self):
        return sorted(self.collection.find().distinct('year'))

    @property
    def variable(self):
        return sorted(self.collection.find().distinct('variable'))


if __name__ == '__main__':
    db = CEICDatabase()
    period = db.period
    print(db.collection)
    print(period)
    print(db.variable)
    print(db.get_variables_from_period_regions(range(2000,2012),['110000','120000','000000']))
    conds = {'region':['110000', '120000', '230600', '230800'],
             'year':['2000', '2001', '2002', '2003', '2004', '2005', '2006'],
             'variable':['从业人员', '从业人数_第一产业', '从业人数_第三产业', '从业人数_第二产业']}
    mdata = db.find(conds)
    print('-----------------------------')
    print(mdata['header'])
    print(mdata['data'])

    '''
    indexdb = Database()
    indexcollection = indexdb.connect('indexDB','CEIC_region')
    print(indexcollection)
    for year in period:
        region_record = db.get_region_by_year(year)
        region_record['year'] = year
        indexcollection.insert(region_record)'''
