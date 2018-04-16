from scrapy import Spider
from scrapy import Request
from scrapingProject.items import BriefItem
import scrapingProject.utilities.data_utilities as du

class InvestingSpider(Spider):
    name = "investingspider"
    allowed_domains = ['investing.com']
    start_urls = ['http://www.investing.com/news/stock-market-news/']
    
    newspaper = 'Investing'
    
    page_number = 17027
    i = 1
    
    def fixTimeFormat(self, date):
        '''
        Given a string that could represents a date in the format " - date_info"
        remove the " - " at the start.
        '''
        date = date.replace(u'\xa0', ' ') # necessary because date contains \xa0 
        s = date.split(" ")
        if s[1] == '-':
            return " ".join(s[2:])    
        return " ".join(s[1:])    
        
    def parse(self, response):
        '''
        Parse a single page from investing.com/news/stock-market-news and yield
        a Request for the next page.
        '''
        # retriving the list of articles for each page
        articles = response.xpath("//article[@class='articleItem']")
        item = BriefItem()
        
        for article in articles:
            try:
                # retriving the date
                item['title'] = article.xpath("//a[@class='title']/text()").extract()[0]
                date = article.xpath("//span[@class='date']/text()").extract()[0]
                # date_time of the current day may be expressed in minutes/hour ago
                if 'ago' in date:
                    item['date'] = du.normalize_timestamp(du.getCurrentDate(), output_format="%Y-%m-%d")
                else:
                    # the date may start with a blank space followed by an '-'
                    date = self.fixTimeFormat(date)
                    date = du.normalize_timestamp(date, output_format="%Y-%m-%d")
                    item['date'] = date
                item['time'] = ""
                url = article.xpath("//a[@class='title']/@href").extract()[0]
                if 'http' not in url:
                    url = "https://www.investing.com" + url
                item['url'] = url
                yield item
            except Exception as e:
                self.logger.error(e)
        # moving to the next page
        if self.i != self.page_number:
            self.i = self.i+1
            yield Request("http://www.investing.com/news/stock-market-news/"+str(self.i))
