# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
import scrapingProject.utilities.data_utilities as du

class AllYouThinkSpider(Spider):
    name = "bigspider"
    allowed_domains = ['moneymorning.com']
    start_urls = ['https://moneymorning.com/sitemap.xml']
    
    newspaper = 'MoneyMorning'
   
    def parse(self, response):
        
            
    def parse_news(self, response):
        """
        Extract the data from the news page and if the page is not in cache,
        this HTML request is counted, so the ip should be updated if necessary.
        The update ip needs to stay here unless you don't want HTTPCACHE
        """
        
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//article/header[@class = "entry-header"]/a/text()')
        loader.add_xpath('title', '//article/header[@class = "entry-header"]/h1/text()')
        loader.add_xpath('author', '//article/header/p/span/a/span[@class = "entry-author-name"]/text()')
        timestamp = response.xpath('//article/header/p/time[@class = "entry-time"]/@datetime').extract()[0]
        timestamp = du.normalize_timestamp(timestamp, hasTimezone = True)
        loader.add_value('date', timestamp.split(' ')[0])
        loader.add_value('time', timestamp.split(' ')[1])
        loader.add_xpath('content', '//article/div[@class= "entry-content"]/p')
        loader.add_xpath('tags', '//meta[@name="news_keywords"]/@content')
        return loader.load_item()
