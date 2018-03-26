import scrapy
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 2

class NYTimesSpider(scrapy.Spider):
    name = "nytspider"
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/section/business/dealbook']
    black_word_list = ["obituaries"]
    allowed_word_list = ["business"]
    NUM_YEAR = 6
    AVG_DAY_PER_SCROLL = 3
    CORRECTIVE_FACTOR = 0.95
    MAX_ITERATION = NUM_YEAR / AVG_DAY_PER_SCROLL * CORRECTIVE_FACTOR * 365
    #MAX_ITERATION = 150
    
    '''
        Filtering news based on the black_world_list.
        If black_world_list isn't defined, return the original list.
        The list is a list of WebElement.
    ''' 
    def filter_news_blacklist(self, links):
        if self.black_word_list == None:
            return links
        
        for item in links:
            item = item.get_attribute("href")
            for word in self.black_word_list:
                if word in item:
                    links.remove(item)
                    break       
        
    '''
        Filtering news based on a list of allowed word.
        If allowed_word_list is not defined, return an empty list.
        The list is a list of WebElement.
    
        TO FIX
        Qui sembra esserci un bug riguardante l'ultimo elemento analizzato
        della lista.
        Testa con:
        links = ['aaa.business/data', 'aaa.ciao/business//', 'www.cordero/business/pro']
        allowed_list = ['business']
        Inoltre c'è un problema nella gestione di \. Prova a scrivere una lista
        così in console e vedi l'output
    '''
    def filter_news_allowed_section(self, links):
        if self.allowed_word_list == None:
            links = []
        
        flag = False
        for item in links:
            item = item.get_attribute("href")
            flag = False
            for word in self.allowed_word_list:
                if word in item:
                    flag = True
                    break
            if flag == False:
                links.remove(item)
        
    
    '''
        Write on file the list of the scraped sites 
        The list is a list of WebElement
    '''
    def write_file(self, file_name, list1):
        try:
            out_file = open(file_name, 'w')
        except:
            self.logger.error("Error opening file: " + file_name)
            return
        try:        
            for t in list1:
                out_file.write(t.get_attribute("href") + "\n")
            out_file.write("\n\n\n")
        except Exception as e:
            self.logger.error("Error writing file: " + file_name)
            self.logger.error(e)
        finally: 
            out_file.close()
    
    
    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)
        driver.find_element_by_xpath(".//button[@class='button load-more-button']").click()
        driver.execute_script("return document.body.scrollHeight")
        
        # Scraping all the links of financial articles avaible in the section Dealbook 
        headline_links = driver.find_elements_by_xpath(".//h2[@class = 'headline']//a")
        
        page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
        flag = False
        i = 0
        try:   
            while flag == False or i < self.MAX_ITERATION: 
                # Handling infinite scroll with both method
                last_count = page_len
                time.sleep(SCROLL_PAUSE_TIME)
                page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
                if last_count == page_len:
                    flag = True
                    self.logger.info("End of page reached")
                i = i + 1 
        except Exception as e:
            self.logger.error("Error scraping dealbook section of nytimes.com")
            self.logger.error(e)
        finally:    
            story_links = driver.find_elements_by_xpath(".//section[@id = 'latest-panel']//a[@class='story-link']")
            
            # Filtering links
            self.filter_news_allowed_section(headline_links)
            self.filter_news_allowed_section(story_links)
            
            # Writing file
            self.write_file("nytimes_news", headline_links)
            self.write_file("nytimes_news", story_links)