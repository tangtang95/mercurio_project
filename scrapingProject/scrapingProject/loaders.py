# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars, strip_html5_whitespace

class NewsLoader(ItemLoader):
    
    default_output_processor = TakeFirst()

    title_in = MapCompose(remove_tags)
    title_out = TakeFirst()

    author_in = MapCompose(strip_html5_whitespace, replace_escape_chars, remove_tags)
    author_out = Join(separator = ',')
    
    date_in = MapCompose(remove_tags)
    date_out = TakeFirst()
    
    time_in = MapCompose(remove_tags)
    time_out = TakeFirst()
    
    #content_in = MapCompose(remove_tags_with_content, which_ones = ('style', ))
    content_out = Join()
    
class BriefLoader(ItemLoader):
    default_output_processor = TakeFirst()