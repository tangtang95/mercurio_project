"""
Created on Sat 17 March 2018

@author: Tang-tang Zhou
"""

from scrapy.spiders import XMLFeedSpider
from scrapy import Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
from scrapingProject.toripchanger import TorIpChanger

NUMBER_OF_REQUEST_PER_IP = 30
SITEMAP_YEAR = '2017'
IP_CHANGER = TorIpChanger(reuse_threshold=10)

class BloombergSpider(XMLFeedSpider):
    name = "bloombergspider"
    allowed_domains = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com/feeds/markets/sitemap_index.xml']
    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    iterator = 'xml'
    itertag = 'n:sitemap'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapingProject.pipelines.ScrapingprojectPipeline': 300
        }
    }
    
    current_ip = 'localhost'
    
    _requests_count = 0
    
    def __init__(self, *args, **kwargs):
        super(BloombergSpider, self).__init__(*args, **kwargs)
        self.current_ip = IP_CHANGER.get_new_ip()

    def update_ip(self):
        """
        After every NUMBER_OF_REQUEST_PER_IP, the spider asks for a new IP
        """
        
        self._requests_count += 1
        if self._requests_count > NUMBER_OF_REQUEST_PER_IP:
            self._requests_count = 0
            self.current_ip = IP_CHANGER.get_new_ip()
    
   
    def parse_node(self, response, node):
        """
        Called everytime the iterator encounters a tag: 'n:sitemap'
        and extract every url that isn't video with the SITEMAP_YEAR in it
        """
        
        sitemap_url = node.xpath('n:loc/text()').extract()[0]
        if 'video' not in sitemap_url and SITEMAP_YEAR in sitemap_url:
            yield Request(sitemap_url, callback = self.parse_month_sitemap)
        
       
    def parse_month_sitemap(self, response):
        """
        Send an HTTP request for every news inside the month sitemap
        """ 
        
        response.selector.register_namespace('n','http://www.sitemaps.org/schemas/sitemap/0.9')
        self.update_ip()
        news_url = response.xpath('n:url/n:loc/text()').extract()
        for url in news_url:
            yield Request(url, callback = self.parse_news)
            
    def parse_news(self, response):
        """
        Extract the data from the news page and if the page is not in cache,
        this HTML request is counted, so the ip should be updated if necessary.
        The update ip needs to stay here unless you don't want HTTPCACHE
        """
        
        if 'cached' not in response.flags:
            self.update_ip()
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//span[@class="lede-text-only__highlight"]/text()')
        loader.add_xpath('title', '//span[@class="lede-large-content__highlight"]/text()')
        loader.add_xpath('title', '//h1[@class="not-quite-full-width-image-lede-text-above__hed"]/text()')
        loader.add_xpath('author', '//div[@class="author"][1]/text()')
        date_time = response.xpath('//time[@class="article-timestamp"]/@datetime').extract()[0]
        loader.add_value('date', date_time[:10])
        loader.add_value('time', date_time[11:19])
        loader.add_xpath('content', '//div[@class="body-copy fence-body"]')
        return loader.load_item()
        
    
