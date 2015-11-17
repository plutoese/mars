# coding=UTF-8

#---------------------------------------------------------------
# class_AdminCodeExcelSheet文件
# @class: AdminCodeExcelSheet类
# @introduction: AdminCodeExcelSheet类用来处理Excel格式的行政区划数据
# @dependency: re，os，DataExcelSheet类
# @author: plutoese
# @date: 2015.11.16
#---------------------------------------------------------------

import re
import pandas as pd
from lib.admincode_lib.class_DataExcelSheet import DataExcelSheet
from lib.database.class_AdminCodeDatabase import AdminCodeDatabase

class AdminCodeDataSheet(DataExcelSheet):
    '''类AdminCodeDataSheet用来处理Excel格式的行政区划数据

    :param str filename: 想要读写的文件名
    :param int,str,list sheet: Excel工作表，可以使工作表号，也可以是工作表名。默认是None，代表所有的工作表。
    :param str version: 版本号，例如'2001_12_31'
    :return: 无返回值
    '''
    def __init__(self, filename=None,sheet=0,version=None):
        DataExcelSheet.__init__(self,filename=filename,sheet=sheet)
        # 设置文件名为版本号，年份为文件名第一部分
        self.version = version
        self.year = re.split('\_',self.version)[0]

        self.data = [[int(row[0]),row[1]] for row in self.rawdata if isinstance(row[0],(int,float))]

        acode = [row[0] for row in self.data]
        region = [row[1] for row in self.data]
        self._data = pd.DataFrame({'region':region},index=acode)
        self.index = self._data.index

        # 连接数据库
        self.db = AdminCodeDatabase()
        self.con = self.db.collection

    # 把数据分类为省地县三级
    def classification(self):
        '''对区域数据进行分级整理

        :return: None
        :var list provinces_dict: 省级行政区划代码字典列表
        :var list prefectures_dict: 地级行政区划代码字典列表
        :var list counties_dict: 县级行政区划代码字典列表
        '''
        index_province =  [code % 10000 == 0 for code in list(self.index)]
        index_prefecture = [code % 10000 != 0 and code % 100 == 0 for code in list(self.index)]
        index_county = [code % 100 != 0 for code in list(self.index)]

        # 创建省地县三级行政区域列表
        self.provinces = self._data[index_province]
        self.prefectures = self._data[index_prefecture]
        self.counties = self._data[index_county]

        self._provinces = pd.DataFrame({'acode':list(self.provinces.index),'region':list(self.provinces['region'])})
        self._prefectures = pd.DataFrame({'acode':list(self.prefectures.index),'region':list(self.prefectures['region'])})
        self._counties = pd.DataFrame({'acode':list(self.counties.index),'region':list(self.counties['region'])})

        # 创建字典形式的三级行政区域，用来插入MongoDB数据库
        self.provinces_dict = [{'acode':str(int(self._provinces.loc[i][0])),'region':self._provinces.loc[i][1],'adminlevel':2,'version':self.version,'year':self.year} for i in self._provinces.index]
        self.prefectures_dict = [{'acode':str(int(self._prefectures.loc[i][0])),'region':self._prefectures.loc[i][1],'adminlevel':3,'version':self.version,'year':self.year} for i in self._prefectures.index]
        self.counties_dict = [{'acode':str(int(self._counties.loc[i][0])),'region':self._counties.loc[i][1],'adminlevel':4,'version':self.version,'year':self.year} for i in self._counties.index]

    def insert(self):
        # 插入的重点在于构建parent
        for item in self.provinces_dict:
            parent = self.con.find({'acode':u'000000'})
            item['parent'] = parent[0]['_id']
            self.con.insert(item)


        for item in self.prefectures_dict:
            parentid = item['acode'][0:2] + u'0000'
            parent = self.con.find_one({'acode':parentid,'version':self.version})
            if parent is None:
                print(parent,item)
                raise NameError
            else:
                item['parent'] = parent['_id']
            self.con.insert(item)

        for item in self.counties_dict:
            parentid = item['acode'][0:4] + u'00'
            parent = self.con.find_one({'acode':parentid,'version':self.version})
            if parent is None:
                item['parent'] = None
                grandpaid = item['acode'][0:2] + u'0000'
                grandpa = self.con.find_one({'acode':grandpaid,'version':self.version})
                if grandpa is None:
                    print('Not good',item)
                    raise NameError
                else:
                    item['parent'] = None
                    item['grandpa'] = grandpa['_id']
            else:
                item['parent'] = parent['_id']
            self.con.insert(item)

if __name__ == '__main__':
    mdatasheet = AdminCodeDataSheet('e:/data/admincode/admincode_1999_2001.xls',sheet=0,version='2001_12_31')
    mdatasheet.classification()
    print(mdatasheet.version)
    print(mdatasheet.year)
    print(mdatasheet.data)

    print(mdatasheet.provinces_dict)
    print(mdatasheet.prefectures_dict)
    print(mdatasheet.counties_dict)

    mdatasheet.insert()




