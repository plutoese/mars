# coding=UTF-8

# --------------------------------------------------------------------------------
# class_ProvinceStatisticsDatabase文件
# @class: ProvinceStatisticsDatabase类
# @introduction:ProvinceStatisticsDatabase类连接ProvinceStatistics数据库集合进行操作
# @dependency: Database
# @author: plutoese
# @date: 2016.01.04
# ---------------------------------------------------------------------------------
"""
.. code-block:: python

    db = MongoDB()
    db.connect('regionDB','CEIC')
"""

import re
import pandas as pd
from webapp.dist.lib.database.class_Database import Database
from webapp.dist.lib.database.class_regionformat import RegionFormat
from pymongo import ASCENDING


class ProvinceStatisticsDatabase(Database):
    """ ProvinceStatisticsDatabase类连接ProvinceStatistics数据库集合进行操作
    """

    def __init__(self):
        Database.__init__(self)
        self.connect('regionDB', 'ProvinceStatistics')
        self.Province_dict = {'130000': '河北省', '440000': '广东省', '610000': '陕西省',
                              '330000': '浙江省', '120000': '天津市', '320000': '江苏省',
                              '640000': '宁夏回族自治区', '500000': '重庆市', '310000': '上海市',
                              '150000': '内蒙古自治区', '360000': '江西省', '450000': '广西壮族自治区',
                              '410000': '河南省', '510000': '四川省', '650000': '新疆维吾尔自治区',
                              '430000': '湖南省', '420000': '湖北省', '620000': '甘肃省',
                              '530000': '云南省', '110000': '北京市', '350000': '福建省',
                              '520000': '贵州省', '140000': '山西省', '220000': '吉林省',
                              '460000': '海南省', '370000': '山东省', '630000': '青海省',
                              '210000': '辽宁省', '340000': '安徽省', '230000': '黑龙江省',
                              '540000': '西藏自治区'}

    def get_region_by_year(self, year):
        """ 获得某年的可选择的区域

        :param str year: 年份
        :return: 区域字典
        :rtype: dict
        """
        region_acode = sorted(self.collection.find({'year': str(year)}).distinct('acode'))
        region_dict = {code: self.Province_dict[code] for code in region_acode}
        return region_dict

    def get_variables_from_period_regions(self,period,regions):
        period = [str(p) for p in period]
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
            projection = {'province':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'unit':1}
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

        if len(mresult.values) < 1:
            return None

        mresult = mresult.drop_duplicates(keep='last')
        cols = mresult.columns.tolist()
        cols[cols.index('province')] = 'region'
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
    db = ProvinceStatisticsDatabase()
    period = db.period
    print(db.collection)
    print(period)
    print(db.variable)
    print(db.get_variables_from_period_regions(range(1980,1982),['110000','120000','000000']))
    projection = {'province':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1}
    conds = {'region':['110000','120000','000000'],'year':['1988','1989'],'variable':[]}
    mdata = db.find(conds)
    print('-----------------------------')
    if 'pdata' in mdata.keys():
        print('yes')
    print((mdata['data']))
    '''
    file = 'd:/down/citydata1.xls'
    mdata['data'].to_excel(file)

    indexdb = Database()
    indexcollection = indexdb.connect('indexDB', 'ProvinceStat_region')
    print(indexcollection)
    for year in period[1:]:
        region_record = db.get_region_by_year(year)
        region_record['year'] = int(year)
        indexcollection.insert(region_record)'''
