# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from w3lib.html import remove_tags, remove_tags_with_content, remove_entities
from w3lib.html import replace_escape_chars, unquote_markup

class ScrapingprojectPipeline(object):
    
    useBriefItemSpider = ['marketwatchspider', 'mktwspider', 
                          "investingspider", 'nytimespider_m','reutersspider']
   
    def open_spider(self, spider):
        """
        This method is scheduled after the spider is opened
        """
        
        self.file = open(spider.name + '_news.tsv', 'w')
        self.newswriter = csv.writer(self.file, delimiter='\t')
        if spider.name in self.useBriefItemSpider:
            self.newswriter.writerow(['title', 'url', 'date', 'time'])
        else:
            self.newswriter.writerow(['title','author','date', 'time', 'content'])

    def close_spider(self, spider):
        """
        This method is scheduled after the spider is closed
        """
        
        self.file.close()
        
    def clean_content(self, text):
        """
        Returns a string of text cleaned up
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
        
        try:
            if spider.name in self.useBriefItemSpider:
                self.newswriter.writerow([item['title'], item['url'], item['date'],
                                          item['time']])
            else:
                item['content'] = self.clean_content(item['content'])
                self.newswriter.writerow([item['title'], item['author'], 
                                          item['date'], item['time'], item['content']])
        except csv.Error as ex:
            self.logger.error(ex)
        self.file.flush()
        return item
