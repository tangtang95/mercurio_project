# -*- coding: utf-8 -*-
'''
Files used to run some temporary scripts regarding utilies, like files 
operation that need to be done only once

This is an example of how to use sentiment_function
'''
import utilities.functions as functions
import sentiment.sentiment_function as sfu
from stanfordcorenlp import StanfordCoreNLP
with StanfordCoreNLP('http://localhost', port=9001, memory='4g') as nlp:
    article = "This is a sentence. For real! It is. Let's test this problem."
    keywords = functions.getKeywords()
    print(sfu.analyze_article(article, keywords, nlp))
    