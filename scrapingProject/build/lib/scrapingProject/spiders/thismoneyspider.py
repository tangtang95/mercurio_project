from scrapy import Spider, Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
import scrapingProject.utilities.data_utilities as du
from datetime import datetime

SITEMAP_YEAR = '2010'

class ThisMoneySpider(Spider):
    name = "thismoneyspider"
    allowed_domains = ['thisismoney.co.uk']
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapingProject.middlewares.RandomUserAgentMiddleware' : 500,
            'scrapingProject.middlewares.ProxyMiddleware' : 400
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(ThisMoneySpider, self).__init__(*args, **kwargs)
        prefix_url = "http://www.thisismoney.co.uk/sitemap-articles-year~"
        suffix_url = ".xml"
        now_year = datetime.now().year
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
        
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//div[@id="js-article-text"]//h1/text()')
        loader.add_xpath('author', '//div[@id="js-article-text"]//a[@class="author"]/text()')
        timestamp = response.xpath('//meta[@property="article:published_time"][1]/@content').extract()[0]
        timestamp = du.normalize_timestamp(timestamp, hasTimezone = True)
        loader.add_value('date', timestamp.split(' ')[0])
        loader.add_value('time', timestamp.split(' ')[1])
        list_of_contents = response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()
        content = ' '.join(list_of_contents)
        loader.add_value('content', content)
        loader.add_xpath('tags', '//meta[@name="keywords"]/@content')
        return loader.load_item()