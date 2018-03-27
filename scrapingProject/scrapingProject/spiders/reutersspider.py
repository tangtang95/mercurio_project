"""
Created on Sat 26 March 2018

@author: Tang-tang Zhou
"""

import datetime
from scrapy import Spider
from scrapy.selector import Selector
from scrapingProject.items import BriefItem
from scrapy import Request
import time

YEAR = '2007'

class ReutersSpider(Spider):
    name = "reutersspider"
    allowed_domains = [ "reuters.com" ]
    start_urls = [ ]
    
    def __init__(self, *args, **kwargs):
        """
        Set up every url for each year to crawl
        """
        super(ReutersSpider, self).__init__(*args, **kwargs)
        prefix_url = "https://www.reuters.com/resources/archive/us/"
        suffix_url = ".html"
        now_year = datetime.datetime.now().year
        #[ self.start_urls.append(prefix_url + str(year) + suffix_url) for year in range(2007, now_year + 1) ]
        self.start_urls.append(prefix_url + YEAR + suffix_url)
    
    def parse(self, response):
        """
        Parse each year archive to get the url for each day of that year
        """
        day_urls = response.xpath('//div[@class="moduleBody"]/p/a/@href').extract()
        for url in day_urls:
            yield Request("https://www.reuters.com" + url, callback = self.parse_news)
            
    def parse_news(self, response):
        """
        Parse all the news inside the page (N.B. inside the content there is only the url)
        """
        list_of_news = response.xpath('//div[@class="headlineMed"]').extract()
        item = BriefItem()
        for news in list_of_news:
            time.sleep(0.1)
            item['title'] = Selector(text=news).xpath('//a/text()').extract()[0]
            item['date'] = response.url[45:49] + "-" + response.url[49:51] + "-" + response.url[51:53]
            time_text = Selector(text=news).xpath('//div/text()').extract()[0]
            time_text = " ".join(time_text.split())
            item['time'] = time_text[0:5] + ":00"
            item['url'] = Selector(text=news).xpath('//a/@href').extract()[0]
            yield item
    
    