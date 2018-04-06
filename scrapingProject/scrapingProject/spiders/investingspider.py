from scrapy import Spider
from scrapy import Request
from scrapingProject.items import BriefItem
import scrapingProject.utilities.data_utilities as du

class InvestingSpider(Spider):
    name = "investingspider"
    allowed_domains = ['investing.com']
    start_urls = ['http://www.investing.com/news/stock-market-news/']
    page_number = 17000
    i = 1
    
    def fixTimeFormat(self, date):
        s = date.split(" ")
        if s[1] == '-':
            return " ".join(s[2:])    
        return " ".join(s[1:])    
        
    def parse(self, response):
        # retriving the list of articles for each page
        articles = response.xpath(".//section[@id='leftColumn']/div[@class='largeTitle']/article")
        item = BriefItem()
        
        for a in articles:
            try:
                # retriving the date
                item['title'] = ''.join(a.xpath(".//div[@class='textDiv']/a/@title").extract())
                date = ''.join(a.xpath(".//div[@class='textDiv']/span[@class='articleDetails']/span[@class='date']/text()").extract())
                if date == "":
                    date = ''.join(a.xpath(".//div[@class='textDiv']/div[@class='articleDetails']/span[@class='date']/text()").extract())
                
                # Date_time of the current time is expressed in minutes/hour ago
                if du.isAgoFormat(str(date)):
                    item['date'] = du.getCurrentDate()
                else:
                    # the date may start with a blank space followed by an '-'
                    date = self.fixTimeFormat(date)
                    item['date'] = date
                item['time'] = ""
                item['url'] = ""
                yield item
            except Exception as e:
                self.logger.error(e)
        # moving to the next page
        if self.i != self.page_number:
            self.i = self.i+1
            yield Request("http://www.investing.com/news/stock-market-news/"+str(self.i))