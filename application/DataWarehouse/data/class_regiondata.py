# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: RegionData
# @introduction: 类RegionData表示区域数据。
# @property:
# @method:
# -----------------------------------------------------------------------------------------

import pandas as pd
from application.DataWarehouse.data.class_data import Data
from application.DataWarehouse.database.class_citystatdatabase import CityStatDatabase


class RegionData:
    '''
    类Data表示行政区划数据
    '''
    # 设置数据库集合
    databases = {'citystatiscs':CityStatDatabase()}

    # 构造函数
    def __init__(self):
        Data.__init__(self)


    # 查询
    def query(self,**conds):
        for key in self.databases:
            result = self.databases[key].find(conds)

        return result

if __name__ == '__main__':
    rdata = RegionData()
    vars = ['年末总人口', '第一产业年末单位从业人员','财政收入']
    #mdata = rdata.query(region=['t'],year=[2010])
    #mdata = rdata.query(region=[['北京']],variable=vars[2],year=[2008,2009,2010])
    #mdata = rdata.query(region=['110000','120000'],variable=vars[2],year=[2008,2009,2010])
    year = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
    year = [int(y) for y in year]
    mdata = rdata.query(region=['110000', '120000'],variable=['财政支出', '财政收入'],year=year)
    print(mdata.keys())
    print(mdata['data'])
    file = 'd:/down/citydata.xls'
    mdata['data'].to_excel(file)


















