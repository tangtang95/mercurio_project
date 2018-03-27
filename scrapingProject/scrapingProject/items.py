# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#date format: yyyy-MM-dd
#time format: whatever

class NewsItem(scrapy.Item):
    
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    
    
    def __init__(self, *args, **kwargs):
        super(NewsItem, self).__init__(*args, **kwargs)
        self['title'] = 'NotFound'
        self['author'] = 'Anonymous'
        self['content'] = 'NotFound'
        self['tags'] = ' '
    

class BriefItem(scrapy.Item):
    
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    
    