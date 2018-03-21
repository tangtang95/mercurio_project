"""
Created on Sat 17 March 2018

@author: Tang-tang Zhou
"""

from scrapy.spiders import XMLFeedSpider
from scrapy import Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
import time

class BloombergSpider(XMLFeedSpider):
    name = "bloombergspider"
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
        news_url = response.xpath('n:url/n:loc/text()').extract()
        for url in news_url:
            time.sleep(0.5)
            yield Request(url, callback = self.parse_news)
        
    def parse_news(self, response):
        l = NewsLoader(item=NewsItem(), response=response)
        l.add_xpath('title', '//span[@class="lede-text-only__highlight"]/text()')
        l.add_xpath('title', '//span[@class="lede-large-content__highlight"]/text()')
        l.add_xpath('title', '//h1[@class="not-quite-full-width-image-lede-text-above__hed"]/text()')
        #self.logger.info("%s: %s", response.url, l.load_item()['title'])
        l.add_xpath('author', '//div[@class="author"][1]/text()')
        l.add_xpath('date', '//time[@class="article-timestamp"]/@datetime')
        l.add_xpath('time', '//time[@class="article-timestamp"]/@datetime')
        l.add_xpath('content', '//div[@class="body-copy fence-body"]')
        return l.load_item()
        
    