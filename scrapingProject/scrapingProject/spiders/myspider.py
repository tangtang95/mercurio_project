"""
Created on Sat 17 March 2018

@author: Tang-tang Zhou
"""

from scrapy.spiders import XMLFeedSpider
from scrapy import Request
from scrapingProject.items import NewsItem
import time

class MySpider(XMLFeedSpider):
    name = "myspider"
    allowed_domains = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com/feeds/markets/sitemap_index.xml']
    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9'),
                  ('x', 'http://www.w3.org/1999/xhtml')]
    iterator = 'xml'
    itertag = 'n:sitemap'
    
    def parse_node(self, response, node):
        sitemap_url = node.xpath('n:loc/text()').extract()[0]
        if 'video' not in sitemap_url:
            yield Request(sitemap_url, callback = self.parse_month_sitemap)
        
    def parse_month_sitemap(self, response):
        response.selector.register_namespace('n','http://www.sitemaps.org/schemas/sitemap/0.9')
        news_url = response.xpath('n:url/n:loc/text()').extract()[0]
        time.sleep(0.05)
        yield Request(news_url, callback = self.parse_news)
        
    def parse_news(self, response):
        pass
        
    