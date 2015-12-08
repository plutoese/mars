# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class SiteScraper:
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
                if link.attrs['href'] not in self.pages:
                    # We have encountered a new page
                    newPage = link.attrs['href']
                    print(newPage)
                    self.pages.add(newPage)
                    self.get_links(newPage)

if __name__ == '__main__':
    site_scraper = SiteScraper("http://www.tianqihoubao.com")
    site_scraper.get_links(page_url="/aqi/",condtion="^(/aqi/)")
