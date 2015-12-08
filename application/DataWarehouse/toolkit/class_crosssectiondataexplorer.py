# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: CrossSectionDataExplorer
# @introduction: 类CrossSectionDataExplorer用来对横截面数据进行数据处理和探索性分析
# @property:
# @method:
# -----------------------------------------------------------------------------------------

import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from application.DataWarehouse.data.class_regiondata import RegionData

class CrossSectionDataExplorer:
    '''
    类CrossSectionDataExplorer用来对横截面数据进行分析处理
    '''
    def __init__(self,data=None):
        self._data = data
        self.index = self._data.index
        self.columns = self._data.columns


class CrossSectionRegionDataExplorer(CrossSectionDataExplorer):
    '''
    类CrossSectionRegionDataExplorer用来对横截面区域数据进行分析处理
    '''
    def __init__(self,data=None):
        CrossSectionDataExplorer.__init__(self,data)
        self.region = self._data['region']

        # 初始化图形接口
        sns.set(style="white", palette="muted", color_codes=True)
        # 设置中文字体
        sns.set_style('white',{"font.sans-serif":  ['Microsoft YaHei','Arial', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']})

    # 概要统计量
    def describe(self):
        return self._data.describe()

    # 最小二乘法
    def ols(self,y=None,x=None):
        y = self._data[y]
        x = pd.DataFrame(self._data[x])
        x.insert(0,'constant',1)
        mod = sm.OLS(y,x)
        res = mod.fit()
        print(res.summary())
        return res

    # 计算相关系数
    def corr(self,vars=None):
        if vars is None:
            return self._data[self.columns[1:]].corr()
        else:
            return self._data[vars].corr()

    # 计算占比变量
    def ratioVar(self,total=None,var=None):
        return self.perVar(pop=total,var=var,weight=100,prefix=u'占比')

    # 计算人均变量
    def perVar(self,pop=None,var=None,weight=None,prefix=u'人均'):
        if isinstance(pop,str):
            pop = self._data[pop]
        if var is None:
            var = self.columns[1:]
        if isinstance(var,str):
            var = [var]
        ndata = {}
        for v in var:
            if weight is None:
                ndata['_'.join([prefix,v])] = self._data[v]/pop
            else:
                ndata['_'.join([prefix,v])] = weight*self._data[v]/pop
        frame = pd.DataFrame(ndata)
        frame.index = self.index
        frame.insert(0, 'region',self._data['region'])
        return frame

    # 计算变量的对数
    def lgVar(self,var=None):
        if var is None:
            var = self.columns[1:]
        if isinstance(var,str):
            var = [var]
        ndata = {}
        for v in var:
            ndata['_'.join([v,u'对数'])] = np.log(self._data[v])
        frame = pd.DataFrame(ndata)
        frame.index = self.index
        frame.insert(0, 'region',self._data['region'])
        return frame

    # 直方图
    def hist(self,var=None,save=False):
        if var is not None:
            sns.distplot(self._data[var])
        else:
            sns.distplot(self._data[self.columns[1:]])
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    # 散点图,kind可以使'reg'和'kde'
    def scatter(self,y=None,x=None,kind='reg',save=False):
        g = sns.jointplot(x=x, y=y, data=self._data, kind=kind)
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    # 散点图矩阵
    def pair(self,vars=None,save=False):
        sns.pairplot(self._data[vars])
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    # 检验一个变量是否为正
    def checkPositive(self,var=None):
        if var is None:
            var = self.columns[1:]
        if isinstance(var,str):
            var = [var]
        for v in var:
            if not (self._data[v]>0).all():
                return False
        return True

    # 储存图像
    def _save(self,savepath='E:/Report/'):
        x = str(int(datetime.now().timestamp()*1000))
        filename = savepath + 'graph/' + x + '.pdf'
        plt.savefig(filename)


if __name__ == '__main__':
    rdata = RegionData()
    mdata = rdata.query(region=['t'],year=[2010],variable=[u'地区生产总值',u'年末总人口'],scale=u'全市')
    mdata = mdata['data']
    csdexplorer = CrossSectionRegionDataExplorer(mdata)
    #dframe = csdexplorer.perVar(pop=mdata[u'年末总人口'],var=[u'地区生产总值',u'年末总人口'])
    #print(dframe)
    '''
    dframe = csdexplorer.lgVar()
    dframe2 = csdexplorer.describe().applymap(lambda x:'{0:.2f}'.format(x))
    print(dframe2)
    csdexplorer.hist(var=u'地区生产总值',save=True)
    csdexplorer.scatter(y=u'地区生产总值',x=u'年末总人口',kind='kde')
    csdexplorer.pair(vars=[u'地区生产总值',u'年末总人口'])'''

    csdexplorer.ols(y=u'地区生产总值',x=u'年末总人口')
    #print(csdexplorer.corr())

    pdata = {'region':['1','2','3'],'x':[1,2,-3],'y':[4,5,6]}
    pdata = pd.DataFrame(pdata)
    cs2 = CrossSectionRegionDataExplorer(pdata)
    print(cs2.checkPositive(var=['y']))
















