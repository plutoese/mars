# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.tianqihoubao.com/aqi/shanghai.html")
bsObj = BeautifulSoup(html.read(),"lxml")
city = bsObj.find('h4')
nameList = bsObj.find("div", {"class":"num"})
print(city.get_text())
#print(bsObj)
#print(bsObj.title)
