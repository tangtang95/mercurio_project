# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    
    def __init__(self, *args, **kwargs):
        super(NewsItem, self).__init__(*args, **kwargs)
        self['title'] = 'default'
        self['author'] = 'default'
        
    
