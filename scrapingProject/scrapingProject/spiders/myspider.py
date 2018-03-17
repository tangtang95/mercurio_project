"""
Created on Sat 17 March 2018

@author: Tang-tang Zhou
"""

from scrapy.spiders import Spider
from scrapingProject.items import ScrapingprojectItem

class MySpider(Spider):
    name = "myspider"
    allowed_domain = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com/feeds/markets/sitemap_index.xml']
    
    def parse(self, response):
        self.logger.info("%s", response.url)

        item = ScrapingprojectItem()
        return item
    