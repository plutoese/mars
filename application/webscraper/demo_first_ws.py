# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json

pages = set()
m_pages = dict()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://www.tianqihoubao.com"+pageUrl)
    bsObj = BeautifulSoup(html, "lxml")
    for link in bsObj.findAll("a", href=re.compile("^(/aqi/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                html_get = urlopen("http://www.tianqihoubao.com" + newPage)
                bsObj_get = BeautifulSoup(html_get, "lxml")
                pages.add(newPage)
                m_pages[newPage] = bsObj_get
                getLinks(newPage)

getLinks("/aqi/")
json.dump(m_pages, fp=open('E:/docs/aqipages.txt', 'w'))
