# coding=UTF-8

from lib.data.class_AdminData import AdminData
from lib.database.class_Database import Database
from werkzeug.datastructures import ImmutableMultiDict
import json

year = list(range(1990,2015))
print(year)

# 利用CEIC的数据来做Demo
# 1. 导入CEIC数据
db = Database()
con = db.connect('regionDB', 'CEIC')
ceic_region_code = sorted(con.find().distinct('acode'))
print(len(ceic_region_code))

# 2. 搜索行政区划代码数据库
admin_data = AdminData()
regions = [admin_data.get_by_acode(acode=acode)[0] for acode in ceic_region_code]

# 3. 生成区域行政数据
region_list = []
for region in regions:
    # 第一个元素是行政区划代码
    if region['adminlevel'] < 3:
        parent = u"中国"
    else:
        parent = admin_data.database.collection.find_one({'_id':region['parent']})
        parent = "/".join(["中国","".join([parent['region'],'属下'])])
    region_list.append([region['acode'],parent,region['region']])
print(region_list)
#json.dump(region_list,fp=open('e:/gitwork/application/testweb/region_ceic.txt', 'w'))

# 4. 查询变量
variables = con.find().distinct('variable')
print(variables)

mdata = ImmutableMultiDict([('period', '1990'), ('period', '1991'), ('period', '1992'), ('period', '1993'), ('period', '1994'), ('period', '1995'), ('period', '1996'), ('period', '1997'), ('period', '1998')])
print(mdata.getlist('period'))




