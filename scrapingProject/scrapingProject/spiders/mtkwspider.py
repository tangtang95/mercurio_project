# -*- coding: utf-8 -*-

from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapingProject.items import BriefItem
from datetime import datetime
import time

ITEMS_TO_PULL = 100
ITERATION = 10

class MKTWSpider(Spider):
    name = "mktwspider"
    allowed_domains = ['www.marketwatch.com/']
    start_urls = ['https://www.marketwatch.com/newsviewer']
    
    
    def __init__(self, *args, **kwargs):
        super(MKTWSpider, self).__init__(*args,**kwargs)
        with open('scrapingProject/JSscripts/getHeadlines.js', 'r') as file:
            self.js_script = file.read()
            
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
        driver = webdriver.Chrome()
        driver.get(response.url)
        
        #removing unncesserary stuff from the page
        driver.execute_script('x=document.getElementById("mktwheadlines"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("rightrail"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("mktwcontrols"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("sponsoredlinks"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("below"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("chrome"); x.parentNode.removeChild(x);')

        driver.execute_script(
            'nv_cont_list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
            'loader = nv_cont_list.getElementsByClassName("loading")[0];'
            'loader.parentNode.removeChild(loader);'
        )
        
        for i in range(ITERATION):
            time.sleep(1)
            driver.execute_script(self.js_script, ITEMS_TO_PULL)
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "loading"))
                )
            except Exception as e:
                self.logger.error(e)
            driver.execute_script('x = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];x.scrollTo(0,x.scrollHeight*3/4);')
            driver.execute_script(
                'nv_cont_list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
                'loader = nv_cont_list.getElementsByClassName("loading")[0];'
                'loader.parentNode.removeChild(loader);'
            )
            elements = driver.find_elements_by_xpath('.//div[@id="thirdpartyheadlines"]//ol[@class="viewport"]/li[not(contains(@class, "loading"))]')
            item = BriefItem()
            last_timestamp_scraped = elements[0].get_attribute("timestamp")
            for elem in elements:
                try:
                    element_data = elem.get_attribute("timestamp")
                    if not(element_data is None) and self.compareTime(element_data, last_timestamp_scraped) :
                        try:
                            item['title'] = elem.find_element_by_xpath('.//div[@class="nv-text-cont"]').text
                        except Exception as e:
                            item['title'] = "#NotFound Title#"
                            
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
            #first get the oldest headline
            #delete all headlines
            #append the oldest headline to the list
            self.logger.info(last_timestamp_scraped)
            driver.execute_script(
                'var elements = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0].getElementsByTagName("li");'
                'var list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
                'while(list.childNodes.length > arguments[0]){'
                'list.removeChild(list.firstChild);}', ITEMS_TO_PULL
      )
            
        