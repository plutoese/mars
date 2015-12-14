# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle

html = urlopen("http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?page=1&scoreSign=3")
bsObj = BeautifulSoup(html.read(),'lxml',from_encoding="UTF-8")
print(bsObj.find(id='queryschoolad'))

driver = webdriver.PhantomJS(executable_path='D:/software/phantomjs-2.0.0-windows/bin/phantomjs')
driver.get("http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?page=5008&scoreSign=3")
time.sleep(3)
table_data = driver.find_element_by_id("queryschoolad").text
print('##############################################')
print(type(table_data))
print(table_data)
driver.close()

F = open('E:/gitwork/application/webscraper/college.pkl', 'wb')
pickle.dump(table_data,F)
F.close()