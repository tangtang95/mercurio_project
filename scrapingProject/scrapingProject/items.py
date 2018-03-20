# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    writer = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    
    def print_csv(file):
        pass
