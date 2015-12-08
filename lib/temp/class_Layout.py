# coding=UTF-8

#from library.region.class_RegionalData import *
from lib.data.class_AdminData import AdminData
import pandas as pd

# 类Layout用于各种数据结构的转换
class Layout:
    '''
    类Layout用于各种数据结构的转换。
    
    属性：
    self.ad: AdminCode的一个实例
    self._data: 读入的数据
    self.year：代表数据的时间，是一个str的列表
    self.acode：代表地区的行政代码，是一个str的list
    self.region：代表地区名称，是一个str的list
    self.variable：代表数据的变量，是一个str的list
    self.ndim：代表数据的维度，是一个字典
    
    方法：
    __init__(self,data=None)：构造函数，用来进行初始化设置。
    _type(self)->dict：辅助函数，用来返回数据的结构类型，无输入参数。返回值是一个字典。：
    stackToNormal(self)：转换数据，从stack格式到normal格式

    Demo：
    转换区域数据的格式，从stack到normal
    ad = AdminCode()
    rdata = RegionalData()    # 构建一个RegionalData的实例
    mdata = rdata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出'],year=2012)    # 查询数据
    lout = Layout(mdata)    # 进行格式转换
    print(lout.stackToNormal())

    得到的结果类似于
           region   财政支出
    330100    杭州市  78628
    330200    宁波市  82844
    330300    温州市  38779
    330400    嘉兴市  26070
    '''
    # 构造函数
    def __init__(self,data=None):
        self.ad = AdminData()
        self._data = data

        self.tags = self._type()
        self.ndim = {'year':len(self.tags['year']),'variable':len(self.tags['variable']),'region':len(self.tags['region'])}

    # 格式转换
    def stackToNormal(self):
        #  构建时间序列数据
        if (self.ndim['variable'] == 1) and (self.ndim['region'] == 1):
            #data = pd.Series(dict(zip(year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])))
            #d = dict(zip(year,data))
            #sname = '|'.join([self.region[0],self.variable[0]])
            #self.tags = [self.region[0],self.variable[0]]
            #self.tags = {'region':self.region[0],'variable':self.variable[0]}
            return pd.Series(dict(zip(self.year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])))

        # 构建横截面数据(地区|变量)
        if self.ndim['year'] == 1:
            g1 = [group for name,group in self._data.groupby(['year'], sort=True)][0]
            g2 = g1.groupby(['variable'], sort=True)
            i = 0
            mdata = []
            for name,data in g2:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.get_by_acode(item)[0]['region'] for item in mdata.index])
            #self.information = self.type['year']
            #self.tags = {'region':}
            return mdata

        # 构建横截面数据(地区|时间)
        if self.ndim['variable'] == 1:
            g = self._data.groupby(['year'], sort=True)
            i = 0
            mdata = []
            for name,data in g:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.get_by_acode(item)[0]['region'] for item in mdata.index])
            #self.information = self.type['variable']
            return mdata

        # panel data
        g = self._data.groupby(['year'], sort=True)
        year = []
        pdata =[]
        for y,g1 in g:
            g2 = g1.groupby(['variable'], sort=True)
            i = 0
            mdata = []
            for name,data in g2:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.get_by_acode(item)[0]['region'] for item in mdata.index])
            year.append(str(y))
            pdata.append(mdata)
        result = pd.Panel(dict(zip(year,pdata)))
        #self.information = []
        return result

    # 辅助函数，返回数据结构
    def _type(self)->dict:
        g = self._data.groupby(['year'], sort=True)
        self.year = [str(name) for name, group in g]

        g = self._data.groupby(['acode'], sort=True)
        self.acode = [name for name, group in g]
        self.region = [self.ad.get_by_acode(item)[0]['region'] for item in self.acode]

        g = self._data.groupby(['variable'], sort=True)
        self.variable = [name for name, group in g]

        return {'year':self.year,'region':self.region,'variable':self.variable}

if __name__ == '__main__':
    ad = AdminCode()
    rdata = RegionalData()
    #mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    mdata = rdata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出'],year=2012)
    #mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=range(2000,2012))
    lout = Layout(mdata)
    print(lout.stackToNormal())
    print(lout.type)
    print(lout.ndim)

    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    g = mdata.groupby(['year'], sort=True)
    print(g)

    for name, group in g:
        print(name)
        print(group)
        print(group['value'])

    print('*****************************************')
    g = group.groupby(['variable'], sort=True)
    i = 0
    for name, group in g:
        print('not',i)
        print(name)
        print(group)
        i = i + 1

    print('-----------------------------------------')
    mdata = lout.stackToNormal()
    print(mdata)
    print(mdata.axes)
    print(mdata['2007'])

    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    mdata = mdata.swapaxes('items','minor')
    mdata = mdata.swapaxes('major','minor')
    print(mdata.to_frame())

