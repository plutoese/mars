# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from application.webscraper.class_SiteScraper import SiteScraper

class AQISite:
    """定期抓取空气后天网站的空气污染数据

    """
    def __init__(self,website='http://www.tianqihoubao.com'):
        self.site_scraper = SiteScraper(website)
        self.pages = self.site_scraper.get_links(page_url="/aqi/",condtion="^(/aqi/)")
        self.data = None

    def daily_aqi_data(self,url_page):
        """抓取每天的空气污染指数

        :param str page: 城市空气污染指数页面
        :return:
        """
        html = urlopen("http://www.tianqihoubao.com" + url_page)
        bsObj = BeautifulSoup(html, "lxml")

if __name__ == '__main__':
    aqi_site = AQISite()