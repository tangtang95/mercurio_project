"""
Created on Sat 26 March 2018

@author: Tang-tang Zhou
"""

from scrapy import Spider, Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
from scrapingProject.toripchanger import TorIpChanger
import datetime

NUMBER_OF_REQUEST_PER_IP = 30
SITEMAP_YEAR = '2010'
IP_CHANGER = TorIpChanger(reuse_threshold=10)

class ThisMoneySpider(Spider):
    name = "thismoneyspider"
    allowed_domains = ['thisismoney.co.uk']
    start_urls = []
    current_ip = "localhost"
    
    _request_count = 0
    
    def update_ip(self):
        """
        After every NUMBER_OF_REQUEST_PER_IP, the spider asks for a new IP
        """
        
        self._requests_count += 1
        if self._requests_count > NUMBER_OF_REQUEST_PER_IP:
            self._requests_count = 0
            self.current_ip = IP_CHANGER.get_new_ip()
    
    def __init__(self, *args, **kwargs):
        super(ThisMoneySpider, self).__init__(*args, **kwargs)
        prefix_url = "http://www.thisismoney.co.uk/sitemap-articles-year~"
        suffix_url = ".xml"
        now_year = datetime.datetime.now().year
        [self.start_urls.append(prefix_url + str(year) + suffix_url) for year in range(2010, now_year + 1)]
        #self.start_urls.append(prefix_url + SITEMAP_YEAR + suffix_url)
        
    
    def parse(self, response):
        response.selector.register_namespace('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urls = response.xpath("//n:sitemap/n:loc/text()").extract()
        for url in urls:
            yield Request(url, callback = self.parse_day_sitemap)
            
    def parse_day_sitemap(self, response):
        response.selector.register_namespace('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        news_urls = response.xpath("//n:url/n:loc/text()").extract()
        for url in news_urls:
            yield Request(url, callback = self.parse_news)
        
    def parse_news(self, response):
        if 'cached' not in response.flags:
            self.update_ip()
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//div[@itemprop="articleBody"]/h1/text()')
        loader.add_xpath('author', '//div[@itemprop="articleBody"]//a[@class="author"]/text()')
        datetime = response.xpath('//meta[@property="article:published_time"][1]/@content')[0]
        loader.add_value('date', datetime[:10])
        loader.add_value('time', datetime[11:19])
        list_of_contents = response.xpath('//div[@itemprop="articleBody"]//p/text()').extract()
        content = ' '.join(list_of_contents)
        loader.add_value('content', content)
        return loader.load_item()