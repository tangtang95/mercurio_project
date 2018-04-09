import scrapy
from selenium import webdriver
import time
from scrapingProject.items import BriefItem
import scrapingProject.utilities.data_utilities as du
from datetime import datetime

SCROLL_PAUSE_TIME = 0.5

class MarketWatchSpider(scrapy.Spider):
    name = "marketwatchspider"
    allowed_domains = ['www.marketwatch.com/']
    start_urls = ['https://www.marketwatch.com/newsviewer']
    
    def parse(self, response):
        '''
        Infinite scroll of market watch news from marketwatch.com/newsviewer
        '''
        driver = webdriver.Firefox()
        driver.get(response.url)
        
        driver.execute_script("x = document.getElementById('mktwheadlines').getElementsByClassName('viewport')[0];")
        
        #removing unncesserary stuff from the page
        driver.execute_script('x=document.getElementById("thirdpartyheadlines"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("rightrail"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("thirdpartycontrols"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("sponsoredlinks"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("below"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("chrome"); x.parentNode.removeChild(x);')
        
        i = 0
        last_timestamp_scraped = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        # Infinite scrolling
        try:   
            while True: 
                time.sleep(SCROLL_PAUSE_TIME)
                driver.execute_script("x = document.getElementById('mktwheadlines').getElementsByClassName('viewport')[0];x.scrollTo(0,x.scrollHeight);")
                i = i + 1
                    
                # Every ten iteration, remove the <li> tags from the web page
                if i % 10 == 0:
                    elements = driver.find_elements_by_xpath('.//div[@id="mktwheadlines"]//ol[@class="viewport"]/li')
                    # Printing retrived elements to the file
                    item = BriefItem()
                    for elem in elements:
                        try:
                            timestamp = elem.get_attribute("timestamp")
                            timestamp = du.normalize_timestamp(timestamp, timezone = 'US/Eastern')
                            if du.compare_time(timestamp, last_timestamp_scraped) :
                                item['title'] = elem.find_element_by_xpath('.//div[@class="nv-text-cont"]').text
                                try:
                                    item['url'] = elem.find_element_by_xpath('.//a[@class="read-more"]').get_attribute("href")
                                except Exception as e:
                                    item['url'] = ""
                                item['date'] = timestamp.split(' ')[0]
                                item['time'] = timestamp.split(' ')[1]
                                last_timestamp_scraped = timestamp
                                
                            yield item        
                        except Exception as e:
                            self.logger.error(e)
                    driver.execute_script('var element = document.getElementsByTagName("li"); var index;for (index = 0; index <= element.length - 2; index++) {element[0].parentNode.removeChild(element[0]);}')
        except Exception as e:
            self.logger.error("Error scraping dealbook section of marketwatch.com")
            self.logger.error(e)
        finally:    
            # need to close the driver
            driver.close()
            