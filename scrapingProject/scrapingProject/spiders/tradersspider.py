from scrapy import Spider
from scrapy import Request
from scrapingProject.items import NewsItem
from scrapingProject.loaders import NewsLoader
import scrapingProject.utilities.data_utilities as du

class TradersSpider(Spider):
    name = "tradersspider"
    allowed_domains = ['4-traders.com']
    start_urls = ['http://www.4-traders.com/news/companies/?p5=456']
    
    newspaper = '4Traders'

    def parse(self, response):
        '''
        Parse a single page from http://www.4-traders.com/news/latest/ and yield
        a Request for each article.
        '''
        # retrieving <a> tag of the next page
        next_page = response.xpath(".//a[@class='nPageEndTab']/@href").extract()
        
        # retrieving the list of articles for each page
        articles = response.xpath(".//table[@id='ALNI0']/tr")
        
        for a in articles:
            try:
                # retriving the data and yielding a request for the single article
                url = a.xpath(".//td[@class='newsColCT ptop3 pbottom3 pleft5 std_txt top ptop3 pbottom3']/a/@href").extract()[0]
                yield Request("http://www.4-traders.com"+url, callback=self.parse_article)                
            except Exception as e:
                self.logger.error(e)
                
        # moving to the next page, if there's one
        if next_page != []:
            yield Request("http://www.4-traders.com/news/companies/"+next_page[0])
        
    def parse_article(self, response):
        '''
        Parse a single article and write requested info to file.
        '''
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', './/h1/text()')
        loader.add_xpath('tags', '//meta[@name="keywords"]/@content')
        loader.add_xpath('tags', '//meta[@name="keywords"]/@content')
        timestamp = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0]
        timestamp = du.normalize_timestamp(timestamp, hasTimezone=True)
        loader.add_value('date', timestamp.split(' ')[0])
        loader.add_value('time', timestamp.split(' ')[1])
        loader.add_xpath('content', './/div[@id="grantexto"]')
        yield loader.load_item()
