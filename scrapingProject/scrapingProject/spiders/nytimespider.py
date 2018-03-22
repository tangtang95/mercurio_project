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
    #MAX_ITERATION = NUM_YEAR / AVG_DAY_PER_SCROLL * CORRECTIVE_FACTOR * 365
    MAX_ITERATION = 10
    
    '''
        Filtering news based on the black_world_list.
        If black_world_list isn't defined, return the original list
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
        If allowed_word_list is not defined, return an empty list
    
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
            if flag == False:
                links.remove(item)
        
    
    '''
        Write on file the list of the scraped sites 
        
        NEED A FIX, Error writing file
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
            out_file.write("\n\n\n")
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
    
        Tuttavia questo metodo proposto, a volte non funziona, quando ad esempio
        si hanno problemi di connessione e la richiesta non carica nulla sul browser
        al momento del controllo. Per quello è stato introdotto anche il metodo
        della stima del numero di iterazioni. Probabilmente è il migliore da
        tenere in considerazione, dato che l'altro consente di eseguire
        uno script piu compatto.
    '''
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
            while flag == False and i < self.MAX_ITERATION: #to_change_with: or
                last_count = page_len
                time.sleep(SCROLL_PAUSE_TIME)
                page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
                if last_count == page_len:
                    flag = True
                i = i + 1    
        except:
            self.logger.error("Error scraping dealbook section of nytimes.com")
        finally:    
            story_links = driver.find_elements_by_xpath(".//section[@id = 'latest-panel']//a[@class='story-link']")
            
            # Filtering links
            headline_links = self.filter_news_allowed_section(headline_links)
            story_links = self.filter_news_allowed_section(story_links)
            
            # Writing file
            self.write_file("nytimes_news", headline_links)
            self.write_file("nytimes_news", story_links)
        
            
        