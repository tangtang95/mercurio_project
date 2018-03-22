import scrapy
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 2

class NYTimesSpider(scrapy.Spider):
    name = "nyspider"
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/section/business/dealbook']
    black_word_list = ["obituaries"]
    allowed_word_list = ["business"]
    
    '''
        Filtering news based on the black_world_list.
        If black_world_list isn't defined, return the original list
        
        TO DO
        Da verificare il passaggio di parametri alle funzioni
    ''' 
    def filter_news_blacklist(self, links):
        if self.black_word_list == None:
            return links
        
        for item in links:
            for word in self.black_word_list:
                if word in item:
                    links.remove(item)
                    break
        return links            
        
    '''
        Filtering news based on a list of allowed word.
        If allowed_word_list is not defined, return an empty list

        TO DO
        Da verificare i parametri delle funzioni
    '''
    def filter_news_allowed_section(self, links):
        if self.allowed_word_list == None:
            return []
        
        flag = False
        for item in links:
            flag = False
            for word in self.allowed_word_list:
                if word in item:
                    flag = True
            if flag == False:
                links.remove(item)
        return links                     
        
    
    '''
        Write on file the list of the scraped sites 
    '''
    def write_file(self, file_name, list1):
        try:
            out_file = open(file_name, 'w')
        except:
            self.logger.error("Error opening file: " + file_name)
            return
        try:        
            for t in list1:
                if self.filter_news(t.get_attribute("href")) == False:
                    out_file.write(t.get_attribute("href") + "\n")
        except: 
            self.logger.error("Error writing file: " + file_name)
        finally: 
            out_file.close()
    

    '''
        TO-DO: 
        Nello scraping di tutti i link di articoli finanziari bisogna fermarsi
        quando trova nella pagina la voce di marzo 2012, al posto del controllo
        sulla variabile contatore i.
        Questa è una pessima strategia, l'operazione di ricerca in una pagine
        molto grande è troppo costosa
        
        https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html
    '''
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
        
        # Filtering links
        headline_links = self.filter_news_allowed_section(headline_links)
        story_links = self.filter_news_allowed_section(story_links)
        
        # Writing file
        self.write_file("nytimes_news", headline_links+story_links)    
    
            
        