# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class WebSiteScraper:
    """用来抓取网站数据
    """
    def __init__(self,website=None):
        # 设置网站地址
        self.website = website

        # 设置网页地址集合
        self.pages = set()

    def get_links(self,page_url,condtion=None):
        html = urlopen(self.website + page_url)
        bsObj = BeautifulSoup(html, "lxml")

        for link in bsObj.findAll("a", href=re.compile(condtion)):
            if 'href' in link.attrs:
                newPage = link.attrs['href']
                newPage = re.sub('\.\./','',newPage)
                if newPage not in self.pages:
                    print(newPage)
                    self.pages.add(newPage)
                    self.get_links(newPage,condtion)

if __name__ == '__main__':
    site_scraper = WebSiteScraper("http://www.cuaa.net/")
    site_scraper.get_links(page_url="cur/",condtion="cur/")
