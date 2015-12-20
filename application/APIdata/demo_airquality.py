# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen
from urllib.parse import urlencode
 
#----------------------------------
# 空气质量调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/33
#----------------------------------
 
def main():
 
    #配置您申请的APPKey
    appkey = "e4c5eabaebe45cad478faf9f65f291f6"
 
    #1.城市空气质量
    request1(appkey,"GET")
 
    #2.城市空气PM2.5指数
    request2(appkey,"GET")
 
    #3.城市空气质量-城市列表
    request3(appkey,"GET")
 
    #4.城市空气PM2.5指数-城市列表
    request4(appkey,"GET")
 
    #5.城市辐射指数
    request5(appkey,"GET")
 
 
 
#城市空气质量
def request1(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/cityair"
    params = {
        "city" : "shanghai", #城市名称的中文名称或拼音，如：上海 或 shanghai
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")
 
#城市空气PM2.5指数
def request2(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/pm"
    params = {
        "city" : "shanghai", #城市名称的中文名称或拼音，如：上海 或 shanghai
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")
 
#城市空气质量-城市列表
def request3(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/airCities"
    params = {
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")
 
#城市空气PM2.5指数-城市列表
def request4(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/pmCities"
    params = {
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")
 
#城市辐射指数
def request5(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/radia"
    params = {
        "city" : "上海", #城市名称的中文拼音，查询城市为“上海”，则输入：上海
        "num" : "", #查询页码数，不写默认为第一页。
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content.decode())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")
 
 
 
if __name__ == '__main__':
    main()
