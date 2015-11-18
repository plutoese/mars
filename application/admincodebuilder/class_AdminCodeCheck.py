# coding=UTF-8

#--------------------------------------------------------------
# class_AdminCodeCheck文件
# @class: AdminCodeCheck类
# @introduction: AdminCodeCheck类用来检查AdminCode数据
# @dependency: re包，pymongo包，Data类，AdminDatabase类
# @author: plutoese
# @date: 2015.11.17
#--------------------------------------------------------------

from lib.database.class_AdminCodeDatabase import AdminCodeDatabase
from lib.data.class_AdminData import AdminData
import pandas as pd

class AdminCodeCheck:
    def __init__(self):
        self.admin_db = AdminCodeDatabase()
        self.admin_data = AdminData()
        self.period = self.admin_db.period

        self.Province = self.admin_data.Province

        self.version = list()
        for y in self.period:
            self.version.extend(self.admin_db.version(y))

    # 测试省级区划
    def admin_checker(self,level='s'):
        no = 1
        for ver in sorted(self.version):
            self.admin_data.set_version(ver)
            self.admin_division = self.admin_data[level]
            admin_division_data = [[p['acode'],p['region']] for p in self.admin_division]
            one_result = pd.DataFrame(admin_division_data,columns=['acode',ver])
            one_result = one_result.set_index('acode')
            if no == 1:
                result = one_result
            else:
                result = pd.merge(result,one_result,left_index=True,right_index=True,how='outer')
            no = no + 1

        return result

    # 另一个角度测试，从每个省级开始
    def admin_division_checker(self,province=None):
        result_prefectures = None
        result_counties = dict()
        result_counties_alone = None

        for ver in sorted(self.version):
            self.admin_data.set_version(ver)
            # 省级行政区划
            province_record = self.admin_data[province]

            if len(province_record) < 1:
                continue

            # 地级行政区划
            prefecture_records = self.admin_data[tuple([province_record[0]['region'],'f'])]
            prefectures = [[p['acode'],p['region']] for p in prefecture_records]
            one_result = pd.DataFrame(prefectures,columns=['acode',ver])
            one_result = one_result.set_index('acode')
            if result_prefectures is None:
                result_prefectures = one_result
            else:
                result_prefectures = pd.merge(result_prefectures,one_result,left_index=True,right_index=True,how='outer')

            # 县级行政区划
            for pre in prefectures:
                county_records = self.admin_data[tuple([province_record[0]['region'],pre[1],'f'])]
                counties = [[p['acode'],p['region']] for p in county_records]
                one_result = pd.DataFrame(counties,columns=['acode',ver])
                one_result = one_result.set_index('acode')
                if result_counties.get(pre[0]) is None:
                    result_counties[pre[0]] = one_result
                else:
                    result_counties[pre[0]] = pd.merge(result_counties[pre[0]],one_result,left_index=True,right_index=True,how='outer')

            county_alone_records = self.admin_data.get_county_children(province=province_record[0]['region'],without_prefecture=True)
            counties_alone = [[p['acode'],p['region']] for p in county_alone_records]
            one_result_alone = pd.DataFrame(counties_alone,columns=['acode',ver])
            one_result_alone = one_result_alone.set_index('acode')
            if result_counties_alone is None:
                result_counties_alone = one_result
            else:
                result_counties_alone = pd.merge(result_counties_alone,one_result_alone,left_index=True,right_index=True,how='outer')

        return {'prefectures':result_prefectures,'counties_with_prefecture':result_counties,'counties_without_prefecture':result_counties_alone}
        #print(len(result_prefectures))
        #print(len(result_counties))
        #print(result_counties_alone)


if __name__ == '__main__':
    checker = AdminCodeCheck()
    result = checker.admin_checker(level='s')
    #print(checker.admin_division)
    #print(result)

    result = checker.admin_division_checker(province=u'重庆')
    result_c1 = result['counties_with_prefecture']
    print(type(result_c1))
    for key in result_c1:
        print(key,result_c1[key])

    result_c2 = result['counties_without_prefecture']
    print(result_c2)