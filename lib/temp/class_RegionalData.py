# coding=UTF-8

from lib.database.class_Database import Database
from lib.data.class_AdminData import AdminData
from lib.temp.class_Layout import Layout
from pymongo import ASCENDING
import pandas as pd
import re

# 类RegionalData用来从数据库MongoDB中导出区域数据
class RegionalData:
    '''
    类RegionalData用来从数据库MongoDB中导出区域数据。
    
    属性：
    self.conn: 数据库MongoDB某集合的接口
    
    方法：
    __init__(self,collection:str='CEIC')：构造函数，参数collection表示集合名称。
    query(self,region:list=None,year:list=None,variable:list=None,projection:dict={'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1},sorts:list=[('year',ASCENDING),('acode',ASCENDING)])->pd.DataFrame：查询返回区域数据。

    Demo：
    查询返回区域数据
    ad = AdminCode()
    rdata = RegionalData()    # 初始化，连接MongoDB中的区域数据
    mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])    # 查询返回区域数据
    mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)    # 查询返回区域数据

    mdata得到的结果
             acode region    value   variable  year
    0   330100    杭州市  27548.0       财政支出  2006
    1   330100    杭州市   1162.4  从业人数_在岗职工  2006
    2   330200    宁波市  29270.0       财政支出  2006
    3   330200    宁波市    887.8  从业人数_在岗职工  2006

    '''
    # 构造函数
    def __init__(self,collection:str='CEIC'):
        # to connect to Mongodb database
        self.collectionname = collection
        self.db = Database()
        self.conn = self.db.connect('regionDB',collection)

    # 获得所有的变量名
    def variables(self):
        posts = self.conn.find()
        return posts.distinct('variable')

    # 从数据库中获取区域数据
    def query(self,region:list=None,year:list=None,variable:list=None,scale:str=None,projection:dict={'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1},sorts:list=[('year',ASCENDING),('acode',ASCENDING)])->pd.DataFrame:
        if region is not None:
            # 如果参数region类型是dict，那么转换为list
            if isinstance(region,dict):
                region = [region]
            # 获得区域的行政代码
            regioncode = [item['acode'] for item in region]
        # 如果参数year类型是str或者int，那么转换为list
        if re.match('^cCity$',self.collectionname) is not None:
            if isinstance(year,int):
                year = [str(year)]
            else:
                year = [str(y) for y in year]
        else:
            if isinstance(year,(int,str)):
                year = [year]
        print(year)
        # 如果参数variable类型是str，那么转换为list
        if isinstance(variable,(str)):
            variable = [variable]

        if (region is not None) and (year is not None) and (variable is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable},'acode':{'$in':regioncode}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable},'acode':{'$in':regioncode},'scale':scale},projection).sort(sorts)))
        elif (region is not None) and (year is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'acode':{'$in':regioncode}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'acode':{'$in':regioncode},'scale':scale},projection).sort(sorts)))
        elif (region is not None) and (variable is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable},'acode':{'$in':regioncode}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable},'acode':{'$in':regioncode},'scale':scale},projection).sort(sorts)))
        elif (year is not None) and (variable is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable},'scale':scale},projection).sort(sorts)))
        elif (region is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'acode':{'$in':regioncode}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'acode':{'$in':regioncode},'scale':scale},projection).sort(sorts)))
        elif(year is not None):
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'scale':scale},projection).sort(sorts)))
        else:
            if scale is None:
                result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable}},projection).sort(sorts)))
            else:
                result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable},'scale':scale},projection).sort(sorts)))
        # 返回的是pd.DataFrame类型
        return result

if __name__ == '__main__':
    ad = AdminData()
    rdata = RegionalData()
    print(rdata.variables())
    mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    #mdata = rdata.query(region=ad[u'浙江',u'f'],variable=u'财政支出',year=2012)
    #mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)
    print(mdata)
    lout = Layout(mdata)
    print(lout.stackToNormal())