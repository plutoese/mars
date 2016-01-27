# coding=UTF-8

#-----------------------------------------------
# class_HospitalDatabase文件
# @class: HospitalDatabase类
# @introduction:HospitalDatabase类连接Hospital数据库集合进行操作
# @dependency: Database
# @author: plutoese
# @date: 2016.01.010
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


class HospitalDatabase(Database):
    """ HospitalDatabase类连接Hospital数据库集合进行操作
    """
    def __init__(self):
        Database.__init__(self)
        self.connect('internetDB', 'Hospital')
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

    # 查询
    def find(self,conds,toStandardForm=True):

        print(conds)
        # 设置projection
        projection = conds.get('projection')
        if projection is None:
            projection = {'province':1,'provinceid':1,'医院名称':1,'医院类别':1,'_id':0,'医院等级':1}
        else:
            conds.pop('projection')
        # 设置sorts
        sorts = conds.get('sorts')
        if sorts is None:
            sorts= [('provinceid',ASCENDING),('医院等级',ASCENDING)]
        else:
            conds.pop('sorts')

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
            conditions['provinceid'] = {'$in': conds['region']}

        result = list(self.collection.find(conditions,projection).sort(sorts))
        mresult = pd.DataFrame(list(self.collection.find(conditions,projection).sort(sorts)))

        if mresult is None:
            return None

        if len(mresult.values) < 1:
            return None

        mresult = mresult.drop_duplicates(keep='last')
        mresult = mresult.fillna('')
        print(mresult)
        cols = mresult.columns.tolist()
        cols[0] = '省份'
        cols[1] = '行政代码'
        print(cols)

        table_data = []
        for i in range(len(mresult.index.tolist())):
            table_data.append(list(mresult.values[i]))

        return {'header':cols,'data':table_data}


    @property
    def grade(self):
        return [item for item in sorted(self.collection.find().distinct('医院等级')) if re.match('^\s+$',item) is not None or len(item) > 0]

    @property
    def type(self):
        return [item for item in sorted(self.collection.find().distinct('医院类别')) if re.match('^\s+$',item) is not None or len(item) > 0]

    @property
    def province(self):
        return sorted(self.collection.find().distinct('province'))

    @property
    def provinceid(self):
        return sorted(self.collection.find().distinct('provinceid'))


if __name__ == '__main__':
    db = HospitalDatabase()
    print(db.collection)
    print(db.grade)
    print(db.type)
    print(db.provinceid)
    print([[id,db.Province_dict[id]]for id in db.provinceid])
    conds = {'region':['110000','120000'],'医院等级':['三级甲等','二级甲等']}
    conds = {'医院等级': ['三级甲等'], '医院类别': ['专科医院', '专科疾病防治所(站、中心)', '专科疾病防治院', '中西医结合医院', '乡镇卫生院', '其他卫生事业机构', '医学专科研究所', '妇幼保健所', '妇幼保健院', '急救中心', '护理院(站)', '民族医院', '疗养院', '社区卫生服务中心', '综合医院', '街道卫生院', '门诊部'], 'region': ['110000', '120000', '130000']}

    mdata = db.find(conds)
    print(mdata)


