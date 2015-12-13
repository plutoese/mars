# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

webs = ['http://www.cuaa.net/cur/2015/index_700',
        'http://www.cuaa.net/cur/2015/03_700',
        'http://www.cuaa.net/cur/2015/04_700',
        'http://www.cuaa.net/cur/2015/05_700',
        'http://www.cuaa.net/cur/2015/06',
        'http://www.cuaa.net/cur/2015/07',
        'http://www.cuaa.net/cur/2015/08',
        'http://www.cuaa.net/cur/2014/',
        'http://www.cuaa.net/cur/2014/02.shtml',
        'http://www.cuaa.net/cur/2014/03.shtml',
        'http://www.cuaa.net/cur/2014/04.shtml',
        'http://www.cuaa.net/cur/2014/05.shtml',
        'http://www.cuaa.net/cur/2014/06.shtml',
        'http://www.cuaa.net/cur/2014/07.shtml',
        'http://www.cuaa.net/cur/2013/01.shtml',
        'http://www.cuaa.net/cur/2013/02.shtml',
        'http://www.cuaa.net/cur/2013/03.shtml',
        'http://www.cuaa.net/cur/2013/04.shtml',
        'http://www.cuaa.net/cur/2013/05.shtml',
        'http://www.cuaa.net/cur/2013/06.shtml',
        'http://www.cuaa.net/cur/2012/',
        'http://www.cuaa.net/cur/2012/02.shtml',
        'http://www.cuaa.net/cur/2012/03.shtml',
        'http://www.cuaa.net/cur/2012/04.shtml',
        'http://www.cuaa.net/cur/2012/05.shtml',
        'http://www.cuaa.net/cur/2012/06.shtml',
        'http://www.cuaa.net/cur/2011/',
        'http://www.cuaa.net/cur/2011/02.shtml',
        'http://www.cuaa.net/cur/2011/03.shtml',
        'http://www.cuaa.net/cur/2011/04.shtml',
        'http://www.cuaa.net/cur/2011/05.shtml',
        'http://www.cuaa.net/cur/2010/pm02.shtml',
        'http://www.cuaa.net/cur/2010/pm03.shtml',
        'http://www.cuaa.net/cur/2010/pm04.shtml',
        'http://www.cuaa.net/cur/2010/pm05.shtml',
        'http://www.cuaa.net/cur/2010/pm06.shtml',
        'http://www.cuaa.net/cur/2009/100.shtml',
        'http://www.cuaa.net/cur/2009/200.shtml',
        'http://www.cuaa.net/cur/2009/300.shtml',
        'http://www.cuaa.net/cur/2009/400.shtml',
        'http://www.cuaa.net/cur/2009/500.shtml',
        'http://www.cuaa.net/cur/2008/zongsu.shtml',
        'http://www.cuaa.net/cur/2008/200.shtml',
        'http://www.cuaa.net/cur/2008/300.shtml',
        'http://www.cuaa.net/cur/2008/400.shtml',
        'http://www.cuaa.net/cur/2008/500.shtml',
        'http://www.cuaa.net/cur/2008/600.shtml',
        'http://www.cuaa.net/cur/2007/zongsu.shtml',
        'http://www.cuaa.net/cur/2007/200.shtml',
        'http://www.cuaa.net/cur/2007/300.shtml',
        'http://www.cuaa.net/cur/2007/400.shtml',
        'http://www.cuaa.net/cur/2007/500.shtml',
        ]

sina_webs = ['http://edu.sina.com.cn/gaokao/2010-01-06/1453232460.shtml','http://edu.sina.com.cn/gaokao/2011-01-17/1136282733.shtml',
             'http://edu.sina.com.cn/gaokao/2009-02-18/1521187603.shtml']

web_obj = []
for web in web_obj:
    html = urlopen(web)
    print(html)
    bsObj = BeautifulSoup(html, "lxml", from_encoding="gb18030")
    print(bsObj)
    web_obj.append(bsObj)

web_sina_obj = []
for web in sina_webs:
    html = urlopen(web)
    bsObj = BeautifulSoup(html, "lxml", from_encoding="gb18030")
    web_sina_obj.append(bsObj)

print(len(web_obj))
'''
F = open('E:/gitwork/application/webscraper/college/collegerating_obj.pkl', 'wb')
pickle.dump(web_sina_obj,F)
F.close()'''


























