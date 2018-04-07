# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapingProject.spiders.marketwatchspider import MarketWatchSpider
from scrapingProject.spiders.investingspider import InvestingSpider

process = CrawlerProcess(get_project_settings())    

process = CrawlerProcess()
process.crawl(MarketWatchSpider)
process.crawl(InvestingSpider)
process.start() # the script will block here until all crawling jobs are finished