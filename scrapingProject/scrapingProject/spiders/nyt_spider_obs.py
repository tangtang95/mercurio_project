import scrapy
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 5

class NYTimesSpider(scrapy.Spider):
    name = "nytspider_obs"
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/section/business/dealbook']
    black_word_list = ["obituaries"]
    allowed_word_list = ["business"]
    NUM_YEAR = 6
    AVG_DAY_PER_SCROLL = 3
    CORRECTIVE_FACTOR = 0.95
    #MAX_ITERATION = NUM_YEAR / AVG_DAY_PER_SCROLL * CORRECTIVE_FACTOR * 365
    MAX_ITERATION = 150
    year = "0" #fix scrauso dovuto al codice di tang tang
    
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
        
        
        STATO DELL'ARTE E ALTERNATIVE PERCORSE
        Essenzialmente per rimuovere elementi bisogna utilizzare degli script 
        javascript, tuttavia i vari articoli sono identificati solamente dall'id
        di conseguenza (oppure dal tag name, tuttavia, avendo provato affermo
        che non ha senso rimuovere per tag name in quanto poi non è piu' possibile
        continuare nello scroll). Di conseguenza la strada che qui si tenta è
        quella di rimuovere tutti gli articoli tramite il loro id, ottenuto tramite
        una query con xpath. 
        Resta un problema sul latest-page-marker che a volte viene cancellato 
        e rimosso dal DOM impedendo di scrollare ancora piu in basso.
    
        Cancellare l'article potrebbe non essere sufficiente
    '''
    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)
        driver.find_element_by_xpath(".//button[@class='button load-more-button']").click()
        driver.execute_script("return document.body.scrollHeight")
        
        # Scraping all the links of financial articles avaible in the section Dealbook 
        headline_links = driver.find_elements_by_xpath(".//h2[@class = 'headline']//a")
        
        delete_list = None
        page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
        flag = False
        scroll_up = False
        i = 0
        prec = ""
        try:   
            while flag == False or i < self.MAX_ITERATION: #to_change_with: or in non debug case
                # Handling infinite scroll with both method
                last_count = page_len
                time.sleep(SCROLL_PAUSE_TIME)
                if scroll_up == True:
                    driver.execute_script("window.scrollTo(0,0);")
                    scroll_up = False
                else:
                    page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
                    
                    if last_count == page_len:
                        flag = True
                        self.logger.info("End of page reached")
                    i = i + 1 
                    
                    '''
                    # deleting articles
                    articles_list = driver.find_elements_by_xpath(".//article[@class='story theme-summary']")
                    driver.execute_script('var element = document.getElementsByClassName("story theme-summary"), index;for (index = element.length - 1; index >= 0; index--) {element[index].parentNode.removeChild(element[index]);}')
                    
                    # every twenty iteration remove the id tag
                    if i % 10 == 0 and i >= 20:
                        id_list = driver.find_elements_by_xpath('.//ol[@id="story-menu-additional-set-latest"]/*')
                        id_list = id_list[:int(len(id_list)/3*2)]
                        for item in id_list:
                            id_value = item.get_attribute("id")
                            driver.execute_script('x=document.getElementById(\"'+id_value+'\"); x.parentNode.removeChild(x);')
                    
                    LEGGI STATO NELL'ARTE NEL COMMENTO SOPRA
                    '''
                
                    # Trying to implement html code remove
                    # Retriving and writing articles' link
                    articles_added = driver.find_elements_by_xpath(".//section[@id = 'latest-panel']//a[@class='story-link']")
                    self.write_file("nytimes_news", articles_added)
                    
                    # Retriving articles' id to remove
                    id_list = driver.find_elements_by_xpath('.//ol[@id="story-menu-additional-set-latest"]/*')
                    
                    # Removing articles from the page by their id
                    for item in id_list:
                        # if the current WebElement doesn't contain an <li> tag with it latest-page-marker, it gets removed
                        try:
                            id_value = item.get_attribute("id")
                        
                            self.logger.info(id_value)
                        
                            if id_value == "latest-page-marker" or "paid-post" in id_value:
                                if "paid-post" in id_value:
                                    last = id_value 
                            else:
                                driver.execute_script('x=document.getElementById(\"'+id_value+'\"); x.parentNode.removeChild(x);')   
                                
                        except Exception as internal_e:
                            self.logger.error("Exception in the for loop")
                            self.logger.error(internal_e)
                    
                    if prec == last:
                        #scroll-up
                        scroll_up = True
                        self.logger.info("here")
                    else:
                        scroll_up = False
                        prec = id_value
                    self.logger.info("A CYCLE HAS BEEN DONE: "+str(i))
                    
        except Exception as e:
            self.logger.error("Error scraping dealbook section of nytimes.com")
            self.logger.error(e)
        finally:    
            #story_links = driver.find_elements_by_xpath(".//section[@id = 'latest-panel']//a[@class='story-link']")
            # Stupid action in order to keep 'finally' not commented
            story_links = None
            self.logger.info("Num of iteration " + str(i))
            
            # Filtering links
            #self.filter_news_allowed_section(headline_links)
            #self.filter_news_allowed_section(story_links)
            
            # Writing file
            #self.write_file("nytimes_news", headline_links)
            #self.write_file("nytimes_news", story_links)
        
            
        