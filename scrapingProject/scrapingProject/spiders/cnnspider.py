from scrapy import Spider, Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
from datetime import datetime
import scrapingProject.utilities.data_utilities as du
from w3lib.html import remove_tags
import string


class CNNSpider(Spider):
    name = "cnnspider"
    allowed_domains = ['money.cnn.com']
    start_urls = []
    current_ip = "localhost"
#    custom_settings = {
#        'DOWNLOADER_MIDDLEWARES' : {
#            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
#            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#            'scrapingProject.middlewares.RandomUserAgentMiddleware' : 500,
#            'scrapingProject.middlewares.ProxyMiddleware' : 400
#        }
#    }
    
    
    def __init__(self, *args, **kwargs):
        super(CNNSpider, self).__init__(*args, **kwargs)
        
        prefix_url = "http://money.cnn.com/registry/sitemaps/articles/"
        suffix_url = ".xml"
        now_year = datetime.now().year
        [self.start_urls.append(prefix_url + str(year) + suffix_url) for year in range(2012, now_year + 1)]
        #self.start_urls.append(prefix_url + SITEMAP_YEAR + suffix_url)
        
    
    def parse(self, response):
        """
        Parse the sitemap of a specific year and send a request of each day_urls
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
        loader.add_xpath('title', '//header//h1/text()')
        translator = str.maketrans('', '', string.punctuation)
        author = ''.join(response.xpath('//span[@class="byline"]').extract())
        author = remove_tags(author).replace("by", '').translate(translator)
        loader.add_value('author', author)
        timestamp = response.xpath('//meta[@name="DC.date.issued"][1]/@content').extract()[0]
        timestamp = du.normalize_timestamp(timestamp, hasTimezone = True)
        loader.add_value('date', timestamp.split(' ')[0])
        loader.add_value('time', timestamp.split(' ')[1])
        list_of_contents = response.xpath(
                '//div[@id="storytext"]/*[not(@class="cnnplayer") and '
                'not(@class="storytimestamp")]').extract()
        content = ' '.join(list_of_contents)
        loader.add_value('content', content)
        loader.add_xpath('tags', '//meta[@name="keywords"]/@content')
        return loader.load_item()