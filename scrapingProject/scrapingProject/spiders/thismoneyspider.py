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
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapingProject.middlewares.RandomUserAgentMiddleware' : 500,
            'scrapingProject.middlewares.ProxyMiddleware' : 400
        }
    }
    
    _requests_count = 0
    
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
        """
        Parse the sitemap of a specific year and send a request of each day_urls
        """
        
        response.selector.register_namespace('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urls = response.xpath("//n:sitemap/n:loc/text()").extract()
        for url in urls:
            yield Request(url, callback = self.parse_day_sitemap)
            
    def parse_day_sitemap(self, response):
        """
        Send a request for each news inside the sitemap from the parse method
        """
        
        response.selector.register_namespace('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        news_urls = response.xpath("//n:url/n:loc/text()").extract()
        for url in news_urls:
            yield Request(url, callback = self.parse_news)
        
    def parse_news(self, response):
        """
        Return a News item with all the content inside the page
        """
        
        if 'cached' not in response.flags:
            self.update_ip()
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//div[@id="js-article-text"]//h1/text()')
        loader.add_xpath('author', '//div[@id="js-article-text"]//a[@class="author"]/text()')
        date_time = response.xpath('//meta[@property="article:published_time"][1]/@content').extract()[0]
        loader.add_value('date', date_time[:10])
        loader.add_value('time', date_time[11:19])
        list_of_contents = response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()
        content = ' '.join(list_of_contents)
        loader.add_value('content', content)
        return loader.load_item()