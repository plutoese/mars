# coding=UTF-8

import re
from DataWarehouse.file.class_Excel import Excel
from DataWarehouse.database.class_database import Database

Province_dict = {'130000': '河北省', '440000': '广东省', '610000': '陕西省',
                              '330000': '浙江省', '120000': '天津市', '320000': '江苏省',
                              '640000': '宁夏回族自治区', '500000': '重庆市', '310000': '上海市',
                              '150000': '内蒙古自治区', '360000': '江西省', '450000': '广西壮族自治区',
                              '410000': '河南省', '510000': '四川省', '650000': '新疆维吾尔自治区',
                              '430000': '湖南省', '420000': '湖北省', '620000': '甘肃省',
                              '530000': '云南省', '110000': '北京市', '350000': '福建省',
                              '520000': '贵州省', '140000': '山西省', '220000': '吉林省',
                              '460000': '海南省', '370000': '山东省', '630000': '青海省',
                              '210000': '辽宁省', '340000': '安徽省', '230000': '黑龙江省',
                              '540000': '西藏自治区'}

Province_dict_reversed = {Province_dict[key]:key for key in Province_dict}
print(Province_dict_reversed)

db = Database()
db._connect('internetDB','Hospital')

filename = 'D:/temp/hospital.xlsx'
mexcel = Excel(filename)
print(mexcel.sheetname)

for province in mexcel.sheetname:
    if province in Province_dict_reversed:
        province_id = Province_dict_reversed[province]
    else:
        print('Not Match: province')

    hospital_list = mexcel.read(sheet=province)
    hospital_list.pop(0)
    for record in hospital_list:
        mongodb_record = {'医院名称':record[0],'医院类别':record[1],'医院等级':record[2],
                          'province':province, 'provinceid':province_id,
                          'source':'中国卫生部医院评审评价项目办公室'}
        print(mongodb_record)
        db.collection.insert(mongodb_record)

