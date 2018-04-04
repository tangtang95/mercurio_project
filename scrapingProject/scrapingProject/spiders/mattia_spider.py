# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:05:02 2018

@author: Mattia
"""

import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class NyTimesSpider(scrapy.Spider):
    #scrapy crawl name
    name = "nytimespider_m"
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/section/business/dealbook']

    def parse(self, response):
        
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.add_argument("--window-size=360,640")
        
        driver = webdriver.Chrome(chrome_options = chrome_options)
        driver.get(response.url)
        
        # Scraping all the links of financial articles avaible in the section Dealbook 
        
        driver.execute_script(
                'var element = document.getElementsByClassName("collection-header"),index;'
                'for (index = element.length - 1; index >= 0; index--){'
                'element[index].parentNode.removeChild(element[index]);}'
                )
        driver.execute_script(
                'element = document.getElementById("site-index");'
                'element.parentNode.removeChild(element);'
                )
        driver.execute_script(
                'element = document.getElementById("page-footer");'
                'element.parentNode.removeChild(element);'
                )
        driver.execute_script(
                'var element = document.getElementsByClassName("tab-navigation"),index;'
                'for (index = element.length - 1; index >= 0; index--){'
                'element[index].parentNode.removeChild(element[index]);}'
                )
        driver.execute_script(
                'var element = document.getElementsByClassName("supplemental"),index;'
                'for (index = element.length - 1; index >= 0; index--){'
                'element[index].parentNode.removeChild(element[index]);}'
                )
        driver.execute_script(
                'var element = document.getElementsByClassName("rank"),index;'
                'for (index = element.length - 1; index >= 0; index--){'
                'element[index].parentNode.removeChild(element[index]);}'
                )
        driver.execute_script(
                'var element = document.getElementsByClassName("story-menu theme-stream initial-set"),index;'
                'for (index = element.length - 1; index >= 0; index--){'
                'element[index].parentNode.removeChild(element[index]);}'
                )
        #//*[@id="story-menu-additional-set-latest"]
        #.//*[@id = 'story-menu-additional-set-latest']//a[@class = 'story-link']
        time.sleep(10)
        i = 0
        try:   
            while i < 80:
                driver.find_element_by_xpath(".//button[@class='button load-more-button']").click()
                i = i + 1 
                
                # deleting article
                #driver.execute_script('var element = document.getElementsByClassName("story theme-summary"), index;for (index = element.length - 1; index >= 0; index--) {element[index].parentNode.removeChild(element[index]);}')
        
        except Exception as e:
            self.logger.error("Error scraping dealbook section of nytimes.com")
            self.logger.error(e)
        finally:
            storylinks = driver.find_elements_by_xpath("//*[@id='story-menu-additional-set-latest']//a[@class = 'story-link']")
            self.logger.info("Num of links " + str(len(storylinks)))
            self.logger.info("Num of iteration " + str(i))
            driver.close()
