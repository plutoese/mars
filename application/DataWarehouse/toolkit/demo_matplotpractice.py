# coding=UTF-8

import matplotlib.pyplot as plt
import seaborn as sns
from application.DataWarehouse.data.class_regiondata import RegionData
from application.DataWarehouse.toolkit.class_crosssectiondataexplorer import CrossSectionRegionDataExplorer

sns.set(style="white", palette="muted", color_codes=True)

# 载入数据
rdata = RegionData()
mdata = rdata.query(region=['t'],year=[2010],variable=[u'地区生产总值',u'年末总人口'],scale=u'全市')
mdata = mdata['data']
csdexplorer = CrossSectionRegionDataExplorer(mdata)
'''
plt.style.use('ggplot')

mdata = mdata[u'地区生产总值']
mdata.plot(kind='hist')
plt.show()
'''

print(sns.axes_style())
sns.set_style('white',{"font.sans-serif":  ['Microsoft YaHei','Arial', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']})

mdata = mdata[u'地区生产总值']
sns.distplot(mdata,kde=False)
plt.show()
