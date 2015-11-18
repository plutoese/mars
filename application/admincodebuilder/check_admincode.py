# coding=UTF-8

from application.admincodebuilder.class_AdminCodeCheck import AdminCodeCheck
from lib.file.class_Excel import Excel
import pandas as pd

# 0. 初始化
checker = AdminCodeCheck()

# 1. 检查时期和版本号
# 时期
periods = checker.admin_db.period
print(periods)
# version
year_versions = [['year','version']]
for y in periods:
    yv = [y]
    yv.extend(checker.admin_db.version(y))
    year_versions.append(yv)
print(year_versions)
year_versions.append([''])
year_versions.append(['注：缺2005_06_30版本'])

# 2. 省、地、县级行政区划
province_checker = checker.admin_checker(level='s')
prefecture_checker = checker.admin_checker(level='t')
county_checker = checker.admin_checker(level='f')

# 3. 另一个角度来看省、地、县级行政区划
writer2 = pd.ExcelWriter('d:/down/admin_checker2.xlsx')
Provinces = checker.Province[0:31]
for prov in Provinces:
    print(prov)
    print(prov['region'])
    result = checker.admin_division_checker(province=prov['region'])
    print(len(result['prefectures']))
    result['prefectures'].to_excel(writer2,sheet_name=prov['region'])
    writer3 = pd.ExcelWriter('d:/down/' + prov['region'] + '_checker3.xlsx')
    result_c1 = result['counties_with_prefecture']

    for key in result_c1:
        result_c1[key].to_excel(writer3,sheet_name=key)

    result_c2 = result['counties_without_prefecture']
    result_c2.to_excel(writer3,sheet_name='no parent')
    writer3.close()


# 0. 输出测试结果
outfile = 'd:/down/check.xlsx'
moutexcel = Excel(outfile).new()
moutexcel.append(year_versions,u'年份和版本号')
moutexcel.close()


writer1 = pd.ExcelWriter('d:/down/admin_checker1.xlsx')
province_checker.to_excel(writer1,sheet_name=u'省级行政区划')
prefecture_checker.to_excel(writer1,sheet_name=u'地级行政区划')
county_checker.to_excel(writer1,sheet_name=u'县级行政区划')

writer1.close()
writer2.close()




