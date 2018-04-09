from scrapy import Spider
from scrapy import Request
import scrapingProject.utilities.data_utilities as du

class TradersSpider(Spider):
    name = "tradersspider"
    allowed_domains = ['4-traders.com']
    start_urls = ['http://www.4-traders.com/news/']
    page_number = 95000
    i = 1

    def parse(self, response):
        '''
        Parse a single page from http://www.4-traders.com/news/latest/ and yield
        a Request for each article.
        '''
        # retriving the list of articles for each page
        articles = response.xpath("")
        
        for a in articles:
            try:
                # retriving the data
                pass
            except Exception as e:
                self.logger.error(e)
                
        # moving to the next page
        if self.i != self.page_number:
            self.i = self.i+1
            yield Request("http://www.4-traders.com/news/latest/?p5="+str(self.i))
            
    def parse_article(self, response):
        '''
        Parse a single article and write requested info to file.
        '''
        pass