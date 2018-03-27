import scrapy
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 0.5

class NYTimesSpider(scrapy.Spider):
    name = "marketwatchspider"
    allowed_domains = ['www.marketwatch.com/']
    start_urls = ['https://www.marketwatch.com/newsviewer']
    MAX_ITERATION = 2
    
    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)
        
        driver.execute_script("x = document.getElementById('mktwheadlines').getElementsByClassName('viewport')[0];")
        
        i = 0
        try:   
            while i < self.MAX_ITERATION: 
                time.sleep(SCROLL_PAUSE_TIME)
                driver.execute_script("x = document.getElementById('mktwheadlines').getElementsByClassName('viewport')[0];x.scrollTo(0,x.scrollHeight);")
                i = i + 1 
        except Exception as e:
            self.logger.error("Error scraping dealbook section of nytimes.com")
            self.logger.error(e)
        finally:    
            # Retriving data
            elements = driver.find_elements_by_xpath('.//div[@id="mktwheadlines"]//ol[@class="viewport"]/li')
            
            # Gettin the value of data and cont for each section
            item = BriefItem()
            for elem in elements:
                try:
                    element_data = elem.get_attribute("timestamp")
                    item['title'] = elem.find_element_by_xpath('.//div[@class="nv-text-cont"]').text
                    item['url'] = elem.find_element_by_xpath('.//a[@class="read-more"]').get_attribute("href")
                    temp = element_data.split(" ")
                    item['date'] = temp[0]
                    item['time'] = temp[1] + " " + temp[2]
                    
                    yield item
                    
                except Exception as e:
                    pass