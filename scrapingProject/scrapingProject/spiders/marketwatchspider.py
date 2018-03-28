import scrapy
from selenium import webdriver
import time
from scrapingProject.items import BriefItem
from datetime import datetime
SCROLL_PAUSE_TIME = 0.5

class MarketWatchSpider(scrapy.Spider):
    name = "marketwatchspider"
    allowed_domains = ['www.marketwatch.com/']
    start_urls = ['https://www.marketwatch.com/newsviewer']
    MAX_ITERATION = 50
    
    def zero_pad_timestamp(self, timestamp):
        '''
            Given a timestamp in the format
            month/day/year hour:minute:second AM/PM
            add a zero pad where needed to month and hour only.
        '''
        x = timestamp.split(" ")
        x[0] = x[0].split("/")
        x[1] = x[1].split(":")
        i = 0
        for i in range(0,2):
            if int(x[i][0]) < 10 and "0" not in x[i][0]:
                x[i][0] = "0"+x[i][0]   
                
        return ""+x[0][0]+"/"+x[0][1]+"/"+x[0][2]+" "+x[1][0]+":"+x[1][1]+":"+x[1][2]+" "+x[2]
           
    
    def compareTime(self, ts1, ts2):
        '''
        Compare timestamp ts1 and ts2. 
        If ts1 < ts2 then return True; false otherwise.
        ts1 and ts2 format must be:
            
        3/27/2018 4:01:29 PM
        '''
        ts1 = self.zero_pad_timestamp(ts1)
        ts2 = self.zero_pad_timestamp(ts2)
        self.logger.error("ts1: "+ ts1)
        self.logger.error("ts2: "+ ts2)
        t1 = datetime.strptime(ts1, "%m/%d/%Y %I:%M:%S %p")
        t2 = datetime.strptime(ts2, "%m/%d/%Y %I:%M:%S %p")
        
        if t1 < t2:
            return True
        return False
    
    def parse(self, response):
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
        last_timestamp_scraped = "03/29/2018 04:15:15 PM" 
        # Infinite scrolling
        try:   
            while i < self.MAX_ITERATION: 
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
                            element_data = elem.get_attribute("timestamp")
                            
                            if self.compareTime(element_data, last_timestamp_scraped) :
                                item['title'] = elem.find_element_by_xpath('.//div[@class="nv-text-cont"]').text
                                try:
                                    item['url'] = elem.find_element_by_xpath('.//a[@class="read-more"]').get_attribute("href")
                                except Exception as e:
                                    item['url'] = ""
                                temp = element_data.split(" ")
                                item['date'] = temp[0]
                                item['time'] = temp[1] + " " + temp[2]
                                last_timestamp_scraped = element_data
                            
                            yield item        
                        except Exception as e:
                            self.logger.error(e)
                    driver.execute_script('var element = document.getElementsByTagName("li"); var index;for (index = 0; index <= element.length - 2; index++) {element[index].parentNode.removeChild(element[index]);}')
        except Exception as e:
            self.logger.error("Error scraping dealbook section of nytimes.com")
            self.logger.error(e)
        finally:    
            # need to close the driver
            #driver.close()
            pass