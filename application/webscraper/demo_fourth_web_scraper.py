# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html,"lxml")

nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList:
    print(name.get_text())

nameList = bsObj.findAll(text="the prince")
print(len(nameList))

'''
html = urlopen("http://sports.sina.com.cn/")
bsObj = BeautifulSoup(html,"lxml")

alist = bsObj.findAll("div")
for a in alist:
    print(a.get_text())'''
