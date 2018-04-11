# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from w3lib.html import remove_tags, remove_tags_with_content, remove_entities
from w3lib.html import replace_escape_chars, unquote_markup
from scrapingProject.items import BriefItem, NewsItem
from scrapingProject.utilities.writers import FileItemWriter, DBItemWriter

import MySQLdb

class ScrapingprojectPipeline(object):
    
    useBriefItemSpider = ['marketwatchspider', 'mktwspider', 
                          "investingspider", 'nytimespider','reutersspider']
   
    def open_spider(self, spider):
        """
        Scheduled after the spider is opened and opens a file in write mode
        """
        if spider.name in self.useBriefItemSpider:
            item_type = BriefItem()
        else:
            item_type = NewsItem()
        self.writer = DBItemWriter(item = item_type, newspaper = spider.newspaper)
        try:
            self.writer.open_writer()
        except Exception as err:
            spider.logger.error(err)
        

    def close_spider(self, spider):
        """
        Scheduled after the spider is closed and closes the file
        """
        self.writer.close_writer()
        
        
    def clean_content(self, text):
        """
        Return a string of text cleaned up by tags, entities,
        escape chars, quotes and spaces
        """
        
        temp = remove_tags_with_content(text, which_ones=('style','script', 'figcaption'))
        temp = remove_tags(temp)
        temp = remove_entities(temp)
        temp = replace_escape_chars(temp)
        temp = unquote_markup(temp)
        temp = " ".join(temp.split())
        return temp
    
    def process_item(self, item, spider):
        '''
        Clean the content and write the item on the file
        '''
        if type(item) is NewsItem:
            item['content'] = self.clean_content(item['content'])
        try:
           self.writer.write_item(item)
        except Exception as err:
            spider.logger.error(err)
        return item
