import scrapy
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 2

class NYTimesSpider(scrapy.Spider):
    name = "nyspider"
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/section/business/dealbook']
    
    
    
    '''
        Filtering news based on the black_world_list.
        If black_world_list isn't defined, return true
        
        TO DO
        Implementare tutto
        Probabilmente sia questa che la write file sono da spostare in un
        file di libreria di funzioni, dato che non sono per nulla legate
        alla classe (? non del tutto sicuro di questa affermazione). 
    ''' 
    def filter_news(self, link, black_word_list = None):
        pass
    
    '''
        Write on file the list of the scraped sites 
    
        TO FIX: chiusura del file se eccezioni presenti
    '''
    def write_file(self, file_name, list1, list2):
        out_file = open(file_name, 'w')
        for t in list1:
            if self.filter_news(t.get_attribute("href")) == False:
                out_file.write(t.get_attribute("href") + "\n")
        for t in list2:
            if self.filter_news(t.get_attribute("href")) == False:
                out_file.write(t.get_attribute("href") + "\n")
        out_file.close()
        
    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)
        driver.find_element_by_xpath(".//button[@class='button load-more-button']").click()
        driver.execute_script("return document.body.scrollHeight")
        
        # Scraping all the links of financial articles avaible in the section Dealbook 
        headline_links = driver.find_elements_by_xpath(".//h2[@class = 'headline']//a")
        
        i = 0
        while i < 12:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            i = i + 1
         
        story_links = driver.find_elements_by_xpath(".//section[@id = 'latest-panel']//a[@class='story-link']")
        
        # Writing file
        self.write_file("nytimes_news", headline_links, story_links)    
    
            
        