# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: CityStatDatabase
# @introduction: 类CityStatDatabase表示城市统计数据库。
# @property:
# - collection: 数据库接口
# @method:
# - connect(db,collection)：连接相应的数据库，参数db是数据库名称，字符串；collection是集合
#                           名称，字符串。无返回值。
# - query(condition,projection,sort): 查询数据库，参数condition是查询条件，字典（详细参见
#                                     pymongo文档；projection是返回结果选择项，字典；sort
#                                     表示排序，列表。返回值是查询得到的数据，列表。
# -----------------------------------------------------------------------------------------

import re
import pandas as pd
from application.DataWarehouse.database.class_database import Database
from application.DataWarehouse.data.class_admindata import AdminData
from application.DataWarehouse.data.class_regionformat import RegionFormat
from pymongo import ASCENDING

class CityStatDatabase(Database):
    '''
    类CityStatDatabase用来连接CityStatistics数据库
    '''

    # 构造函数
    def __init__(self):
        # 连接CityStatistics集合
        Database.__init__(self)
        #self._connect('regionDB','CityStatistics')
        self._connect('regionDB','CEIC')
        self.ad = AdminData()

    # 查询
    def find(self,conds,toStandardForm=True):

        print(conds)
        # 设置projection
        projection = conds.get('projection')
        if projection is None:
            projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
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
            period = period
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
                self.ad.setYear(year)
                if re.match('^[0-9]{6}$',conds['region'][0]) is not None:
                    conditions['acode'] = {'$in': conds['region']}
                else:
                    conditions['acode'] = {'$in':[region['acode'] for item in conds['region'] for region in self.ad[tuple(item)]]}
                #print(conditions['acode'])
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

        if toStandardForm:
            rformat = RegionFormat(mresult)
            return rformat.transform()
        else:
            return mresult

    @property
    def variables(self):
        return self.collection.find().distinct('variable')

    # 获得变量所有的时期
    def period(self,variable):
        print(variable)
        if isinstance(variable,str):
            posts = self.collection.find({'variable':variable}).distinct('year')
        else:
            posts = set()
            for var in variable:
                periods = self.collection.find({'variable':var}).distinct('year')
                posts.update(periods)
            posts = list(posts)
        return sorted(posts)


if __name__ == '__main__':
    db = CityStatDatabase()
    print(db.variables)
    print(db.collection)
    projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
    #conds = {'region':[[u'上海'],[u'浙江',u'杭州市']],'year':[2010],'variable':[u'人均地区生产总值',u'职工平均工资'],'scale':u'全市','projection':projection}
    conds = {'region':[u't'],'year':[2012],'variable':[u'财政支出'],'projection':projection}
    mdata = db.find(conds)
    print('-----------------------------')
    print(mdata)


















