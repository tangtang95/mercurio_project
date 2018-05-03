from datetime import datetime as DT
from scrapy import Spider
from scrapy.selector import Selector
from scrapingProject.items import BriefItem
from scrapy import Request
import scrapingProject.utilities.data_utilities as du

#YEAR = '2007'

class ReutersSpider(Spider):
    name = "reutersspider"
    allowed_domains = [ "reuters.com" ]
    start_urls = [ ]
    newspaper = 'Reuters'
    
    def __init__(self, *args, **kwargs):
        """
        Set up every url for each year to crawl
        """
        
        super(ReutersSpider, self).__init__(*args, **kwargs)
        prefix_url = "https://www.reuters.com/resources/archive/us/"
        suffix_url = ".html"
        now_year = DT.now().year
        [ self.start_urls.append(prefix_url + str(year) + suffix_url) for year in range(2007, now_year + 1) ]
        #self.start_urls.append(prefix_url + YEAR + suffix_url)
    
    def parse(self, response):
        """
        Parse each year archive to get the url for each day of that year
        """
        
        day_urls = response.xpath('//div[@class="moduleBody"]/p/a/@href').extract()
        for url in day_urls:
            yield Request("https://www.reuters.com" + url, callback = self.parse_news)
            
    def parse_news(self, response):
        """
        Parse all the news inside the page
        """
        
        list_of_news = response.xpath('//div[@class="headlineMed"]').extract()
        item = BriefItem()
        for news in list_of_news:
            item['title'] = Selector(text=news).xpath('//a/text()').extract()[0]
            timestamp = response.url[45:53] + " " + Selector(text=news).xpath('//div/text()').extract()[0]   
            timestamp = du.normalize_timestamp(timestamp)
            item['date'] = timestamp.split(' ')[0]
            item['time'] = timestamp.split(' ')[1]
            item['url'] = Selector(text=news).xpath('//a/@href').extract()[0]
            yield item
    
    