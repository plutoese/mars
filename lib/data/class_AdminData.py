# coding=UTF-8

#--------------------------------------------------------------
# class_AdminData文件
# @class: AdminData类
# @introduction: AdminData类表示行政区划数据
# @dependency: re包，pymongo包，Data类，AdminDatabase类
# @author: plutoese
# @date: 2015.10.18
#--------------------------------------------------------------

'''
.. code-block:: python

    adata = AdminData(year=2004)
    print(adata.version)
    print(adata.Province)
    print(adata.get_province_by_name(u'浙江'))
    print(adata.get_prefecture_children(u'浙江'))
    print(adata.get_prefecture_by_name(province=u'浙江',prefecture=u'嘉兴市'))
    print(adata.get_county_children(province=u'浙江',prefecture=u'嘉兴市'))
    print(adata.get_county_by_name(province=u'浙江',prefecture=u'嘉兴市',county=u'平湖市'))

    print(adata.get_by_acode('220000'))
    print(adata.ProvincePrefecture)

    print(adata[u'浙江','b'])
    print(adata[u'浙江',u'嘉兴',u'孩孩'])

    adata.set_year(2010)
    print(adata[tuple([u'浙江',u'f'])])
    print(adata[tuple([u'北京'])])
'''

import re
from lib.data.class_Data import Data
from lib.database.class_AdminDatabase import AdminDatabase
from pymongo import ASCENDING

class AdminData:
    '''AdminData类表示行政区域数据

    :param str version: 颁布的行政区划的版本号
    :param int,str year: 颁布的行政区划的年份
    :var AdminDatabase database: 行政区划数据库
    :var str latestversion: 最新颁布的行政区划版本号
    :var str year: 年份
    :var str version: 版本号
    :var list Province: 某个版本的所有省级行政区划
    :var list Prefecture: 某个版本的所有地级行政区划
    :var list County: 某个版本的所有县级行政区划
    :var list ProvincePrefecture: 某个版本的所有省级和地级行政区划
    :var list ProvincePrefectureCounty: 某个版本的所有省级地级县级区划

    通用接口__getitem__

    :param str,list key: 查询条件。其中的key表示表示区域名称，方法如下：
    （1）省级区域，用名字直接表示，例如ad[u'北京']；
    （2）地级区域，用省级、地级名称表示，例如ad[u'浙江',u'嘉兴']；（3）县级区域，用省级、地级、县级名称表示，例如ad[u'湖北', u'恩施',u'来凤']；
    （4）如果是本级行政区域加上下级行政区域，下级行政区域用f（first）表示，例如表示浙江省及其所有地级行政区域，用ad[u'浙江',u'f']；
    （5）如果是本级行政区域加上下下级行政区域，下下级行政区域用s（second）表示，例如表示浙江省及其所有县级行政区域，用ad[u'浙江',u's']；
    （6）如果是本级行政区域加上下级及下下级行政区域，下级及下下级行政区域用b（both）表示，例如表示浙江省及其所有地县级行政区域，用ad[u'浙江',u'b']。返回值是数据库中查询得到的行政区划的列表。
    '''
    def __init__(self,version=None,year=None):
        Data.__init__(self)
        # 设置数据库
        self.database = AdminDatabase()

        # 设置最新版本
        self.latestversion = self.database.version()[-1]

        # 设置版本和年份
        if (version is None) and (year is None):
            self.version = self.latestversion
            self.year = re.split('_',self.version)[0]
        elif version is not None:
            self.version = version
            self.year = re.split('_',self.version)[0]
        else:
            self.year = str(year)
            self.version = self.database.version(self.year)[-1]

    # 通用行政区划查询接口
    def __getitem__(self, key):
        '''通用行政区划查询接口

        :param key:
        :return: 查询结果
        '''
        # f to get all first level
        # s to get all second level
        # b to get all first and second level
        if isinstance(key,str):
            if re.match('^s$',key):
                return self.Province
            if re.match('^t$',key):
                return self.Prefecture
            if re.match('^f$',key):
                return self.County
            return self.get_province_by_name(key)

        if isinstance(key,tuple) and len(key) < 2:
            if re.match('^s$',key[0]):
                return self.Province
            if re.match('^t$',key[0]):
                return self.Prefecture
            if re.match('^f$',key[0]):
                return self.County
            return self.get_province_by_name(key[0])

        if isinstance(key,tuple):
            if len(key) < 3:
                if re.match(key[1],u'f') is not None:
                    result = self.get_prefecture_children(key[0])
                    return self._sorted(result)
                elif re.match(key[1],u's') is not None:
                    prefectures = self.get_prefecture_children(key[0])
                    result = []
                    for item in prefectures:
                        result.extend(self.get_county_children(key[0],item['region']))
                    return self._sorted(result)
                elif re.match(key[1],u'b') is not None:
                    prefectures = self.get_prefecture_children(key[0])
                    result = []
                    for item in prefectures:
                        result.append(item)
                        result.extend(self.get_county_children(key[0],item['region']))
                    return self._sorted(result)
                else:
                    return self.get_prefecture_by_name(key[0],key[1])
            else:
                if re.match(key[2],u'f') is not None:
                    result = self.get_county_children(key[0],key[1])
                    return self._sorted(result)
                else:
                    return self.get_county_by_name(key[0],key[1],key[2])

    def get_by_acode(self,acode,year=None):
        '''通过行政区划代码（acode)查询行政区划

        :param str acode: 行政区划代码
        :param int,str year: 年份
        :return: 查询结果
        :rtype: list
        '''
        if year is None:
            return list(self.database.find(acode=acode,version=self.version))
        else:
            version = self.database.version(year)[-1]
            return list(self.database.find(acode=acode,version=version))

    def get_province_by_name(self,province):
        '''通过省级名称查询行政区划

        :param str province: 省级行政区划名称
        :return: 省级行政区划单位
        :rtype: list
        '''
        province_pattern = u'省|市|自治区|维吾尔自治区|回族自治区|壮族自治区'
        province = re.split(province_pattern,re.sub('\s+','',province))[0]
        mprovince = '^' + province +'$'
        result = [item for item in self.Province if re.match(mprovince,re.split(province_pattern,item['region'])[0]) is not None]
        if len(result) < 1:
            return []
        return  result

    def get_prefecture_by_name(self,province,prefecture):
        '''通过省级地级名称查询行政区划

        :param str province: 省级行政区划名称
        :param str prefecture: 地级行政区划名称
        :return: 地级行政区划单位
        :rtype: list
        '''
        prefectures =  self.get_prefecture_children(province)
        result = [item for item in prefectures if re.match(prefecture,item['region']) is not None]
        if len(result) < 1:
            return []
        return result

    # 获得一个县级单位
    def get_county_by_name(self,province,prefecture,county):
        '''通过省级地级县级名称查询行政区划

        :param str province: 省级行政区划名称
        :param str prefecture: 地级行政区划名称
        :param str county: 县级行政区划名称
        :return: 县级行政区划单位
        :rtype: list
        '''
        counties =  self.get_county_children(province,prefecture)
        result = [item for item in counties if re.match(county,item['region']) is not None]
        if len(result) < 1:
            return []
        return result

    def get_prefecture_children(self,province):
        '''通过省级名称获得其辖区下的所有地级行政区划

        :param str province: 省级行政区划的名称
        :return: 某省级单位辖区下的所有地级区划单位
        :rtype: list
        '''
        province_found = self.get_province_by_name(province)
        if len(province_found) < 1:
            print('Can not find ',province)
            raise NameError
        if len(province_found) > 1:
            print('Tow much: ',province)
            raise NameError
        prefecture = self.database.find(parent=province_found[0]['_id'],version=self.version,sorts=[('acode',ASCENDING)])
        return list(prefecture)

    def get_county_children(self,province,prefecture):
        '''通过省级和地级区域名称获得其辖区下的所有县级行政区划

        :param str province: 省级行政区划名称
        :param str prefecture: 地级行政区划名称
        :return: 某个地级行政单位辖区下的所有县级区划单位
        :rtype: list
        '''
        # to find province item
        prefecture_found = self.get_prefecture_by_name(province,prefecture)
        if len(prefecture_found) < 1:
            print('Can not find ',province,'.',prefecture)
            raise NameError
        if len(prefecture_found) > 1:
            print('Tow much: ',province,'.',prefecture)
            raise NameError
        county = self.database.find(parent=prefecture_found[0]['_id'],version=self.version,sorts=[('acode',ASCENDING)])
        return list(county)

    # 设置版本
    def set_version(self,version):
        '''设置版本号

        :param str version: 颁布的行政区划版本号
        :return: 无返回值
        '''
        self.version = version
        self.year = re.split('_',self.version)[0]

    # 设置年份
    def set_year(self,year):
        '''设置年份

        :param str year: 年份
        :return: 无返回值
        '''
        self.year = str(year)
        self.version = self.database.version(self.year)[-1]

    # 所有的省级单位
    @property
    def Province(self):
        return self._sorted(list(self.database.find(adminlevel=2,version=self.version)))

    # 所有的省级单位
    @property
    def Prefecture(self):
        return self._sorted(list(self.database.find(adminlevel=3,version=self.version)))

    # 所有的省级单位
    @property
    def County(self):
        return self._sorted(list(self.database.find(adminlevel=4,version=self.version)))

    # 获得省级和地级单位
    @property
    def ProvincePrefecture(self):
        result = []
        provinces = self.Province
        for province in provinces:
            result.append(province)
            result.extend(self.get_prefecture_children(province['region']))
        return result

    # 获得省级、地级和县级单位
    @property
    def ProvincePrefectureCounty(self):
        result = []
        provinces = self.Province
        for province in provinces:
            result.append(province)
            prefectures = self.get_prefecture_children(province['region'])
            for prefecture in prefectures:
                result.append(prefecture)
                result.extend(self.get_county_children(province['region'],prefecture['region']))
        return result

    # 辅助排序函数
    def _sorted(self,regions):
        if len(regions) < 1:
            return []
        return sorted(regions,key = lambda x:x['acode'])


if __name__ == '__main__':
    adata = AdminData(year=2004)

    print(adata.version)
    print(adata.Province)
    print(adata.get_province_by_name(u'浙江'))
    print(adata.get_prefecture_children(u'浙江'))
    print(adata.get_prefecture_by_name(province=u'浙江',prefecture=u'嘉兴市'))
    print(adata.get_county_children(province=u'浙江',prefecture=u'嘉兴市'))
    print(adata.get_county_by_name(province=u'浙江',prefecture=u'嘉兴市',county=u'平湖市'))

    print(adata.get_by_acode('220000'))
    print(adata.ProvincePrefecture)

    print(adata[u'浙江','b'])
    print(adata[u'浙江',u'嘉兴',u'孩孩'])

    adata.set_year(2010)
    print(adata[tuple([u'浙江',u'f'])])
    print(adata[tuple([u'北京'])])

















