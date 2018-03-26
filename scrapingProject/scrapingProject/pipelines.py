# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from w3lib.html import remove_tags, remove_tags_with_content, remove_entities
from w3lib.html import replace_escape_chars, unquote_markup

class ScrapingprojectPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '_news.tsv', 'w')
        self.newswriter = csv.writer(self.file, delimiter='\t')
        self.newswriter.writerow(['title','author','date', 'time', 'content'])

    def close_spider(self, spider):
        self.file.close()
        
    def clean_content(self, text):
        temp = remove_tags_with_content(text, which_ones=('style','script',))
        temp = remove_tags(temp)
        temp = remove_entities(temp)
        temp = replace_escape_chars(temp)
        temp = unquote_markup(temp)
        temp = " ".join(temp.split())
        return temp
    
    def process_item(self, item, spider):
        item['content'] = self.clean_content(item['content'])
        try:
            self.newswriter.writerow([item['title'], item['author'], 
                                     item['date'], item['time'], item['content']])
        except csv.Error as ex:
            self.logger.error(ex)
        self.file.flush()
        return item
