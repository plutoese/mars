from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.tianqihoubao.com/aqi/")
bsObj = BeautifulSoup(html,'lxml')
for link in bsObj.findAll("a",href=re.compile("^(/aqi/)[a-zA-Z0-9]*.html")):
    if 'href' in link.attrs:
        print(link.attrs['href'])