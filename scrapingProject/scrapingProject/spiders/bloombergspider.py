from scrapy import Spider
from scrapy import Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
import scrapingProject.utilities.data_utilities as du
from w3lib.html import replace_escape_chars, strip_html5_whitespace

SITEMAP_YEAR = '2015'

class BloombergSpider(Spider):
    name = "bloombergspider"
    allowed_domains = ['bloomberg.com']
    start_urls = ['https://www.bloomberg.com/feeds/markets/sitemap_index.xml']  
#    custom_settings = {
#        'DOWNLOADER_MIDDLEWARES' : {
#            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
#            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#            'scrapingProject.middlewares.RandomUserAgentMiddleware' : 500,
#            'scrapingProject.middlewares.ProxyMiddleware' : 400
#        }
#    }
    
   
    def parse(self, response):
        """
        Called everytime the iterator encounters a tag: 'n:sitemap'
        and extract every url that isn't video with the SITEMAP_YEAR in it
        """
        response.selector.register_namespace('n','http://www.sitemaps.org/schemas/sitemap/0.9')
        sitemap_urls = response.xpath('//n:loc/text()').extract()
        for sitemap_url in sitemap_urls:
            if 'video' not in sitemap_url and SITEMAP_YEAR in sitemap_url:
                yield Request(sitemap_url, callback = self.parse_month_sitemap)
        
       
    def parse_month_sitemap(self, response):
        """
        Send an HTTP request for every news inside the month sitemap
        """ 
        
        response.selector.register_namespace('n','http://www.sitemaps.org/schemas/sitemap/0.9')
        news_url = response.xpath('//n:url/n:loc/text()').extract()
        for url in news_url:
            yield Request(url, callback = self.parse_news)
            
    def parse_news(self, response):
        """
        Extract the data from the news page and if the page is not in cache,
        this HTML request is counted, so the ip should be updated if necessary.
        The update ip needs to stay here unless you don't want HTTPCACHE
        """
        
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//span[@class="lede-text-only__highlight"]/text()')
        loader.add_xpath('title', '//span[@class="lede-large-content__highlight"]/text()')
        loader.add_xpath('title', '//article//h1/text()')
        authors = response.xpath('//div[@class="author"]/text()').extract()
        for author in authors:
            author = strip_html5_whitespace(author)
            author = replace_escape_chars(author)
            if len(author) != 0:
                loader.add_value('author', author)
        timestamp = response.xpath('//time[@class="article-timestamp"]/@datetime').extract()[0]
        timestamp = du.normalize_timestamp(timestamp, hasTimezone = True)
        loader.add_value('date', timestamp.split(' ')[0])
        loader.add_value('time', timestamp.split(' ')[1])
        loader.add_xpath('content', '//div[@class="body-copy fence-body"]')
        loader.add_xpath('tags', '//meta[@name="keywords"]/@content')
        return loader.load_item()
        
    
