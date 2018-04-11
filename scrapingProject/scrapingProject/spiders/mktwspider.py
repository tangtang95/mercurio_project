from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapingProject.items import BriefItem
import scrapingProject.utilities.data_utilities as du
from datetime import datetime
import time

ITEMS_TO_PULL_FOR_REQUEST = 1000
ITEMS_TO_KEEP = 30

class MKTWSpider(Spider):
    name = "mktwspider"
    allowed_domains = ['marketwatch.com']
    start_urls = ['https://www.marketwatch.com/newsviewer']
    
    newspaper = 'WallStreetJournal'
    
    
    def __init__(self, *args, **kwargs):
        super(MKTWSpider, self).__init__(*args,**kwargs)
        with open('scrapingProject/JSscripts/getHeadlines.js', 'r') as file:
            self.js_script = file.read()

    def parse(self, response):
        """
        Parse the start_urls with selenium
        """
        driver = webdriver.Firefox()
        driver.get(response.url)
        
        #removing unncesserary stuff from the page
        driver.execute_script('x=document.getElementById("mktwheadlines"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("rightrail"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("mktwcontrols"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("sponsoredlinks"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("below"); x.parentNode.removeChild(x);')
        driver.execute_script('x=document.getElementById("chrome"); x.parentNode.removeChild(x);')

        #remove the tag li:loading from the list
        driver.execute_script(
            'nv_cont_list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
            'loader = nv_cont_list.getElementsByClassName("loading")[0];'
            'loader.parentNode.removeChild(loader);'
        )
        
        last_timestamp_scraped = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        while True:
            time.sleep(1)
            
            #executes the script to get the news item and then append the tag 
            #li:loading at the end of the list
            driver.execute_script(self.js_script, ITEMS_TO_PULL_FOR_REQUEST)
            try:
                #wait until the tag li:loading reappers
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "loading"))
                )
            except Exception as e:
                self.logger.error(e)
            #scroll the list <ul> to more than a half of its height to avoid
            #the downloading of newer news
            driver.execute_script(
                    'x = document.getElementById("thirdpartyheadlines")'
                                '.getElementsByTagName("ol")[0];'
                    'x.scrollTo(0,x.scrollHeight*3/4);'
            )
            #remove the tag li:loading from the list
            driver.execute_script(
                'nv_cont_list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
                'loader = nv_cont_list.getElementsByClassName("loading")[0];'
                'loader.parentNode.removeChild(loader);'
            )
            #retrieving the list of news
            elements = driver.find_elements_by_xpath('.//div[@id="thirdpartyheadlines"]//ol[@class="viewport"]/li[not(@class="loading")]')
            item = BriefItem()
            for elem in elements:
                try:
                    timestamp = elem.get_attribute("timestamp")
                    timestamp = du.normalize_timestamp(timestamp, timezone = 'US/Eastern')
                    if du.compare_time(timestamp, last_timestamp_scraped):
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
            #delete the newer headlines until remains "ITEMS_TO_KEEP" news
            self.logger.info(last_timestamp_scraped)
            driver.execute_script(
                'var elements = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0].getElementsByTagName("li");'
                'var list = document.getElementById("thirdpartyheadlines").getElementsByTagName("ol")[0];'
                'while(list.childNodes.length > arguments[0]){'
                'list.removeChild(list.firstChild);}', ITEMS_TO_KEEP)
        driver.close()
            
        