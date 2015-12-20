# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle

# 0. set up parameters
START = 3686
STOP = 5000
#PhantomJS_path = 'D:/Tools/phantomjs-2.0.0-windows/bin/phantomjs'
PhantomJS_path = 'D:/software/phantomjs-2.0.0-windows/bin/phantomjs'
DRIVER = webdriver.PhantomJS(executable_path=PhantomJS_path)

# 1. load website
for i in range(START,STOP):
    url_load = 'http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?page={}&scoreSign=3'.format(i)
    DRIVER.get(url_load)
    time.sleep(5)
    table_data = DRIVER.find_element_by_id("queryschoolad").text
    print(table_data)
    print('*****************',i,'************************')

    file_path = 'E:/Data/college/c{}.pkl'.format(i)
    F = open(file_path, 'wb')
    pickle.dump(table_data,F)
    F.close()


