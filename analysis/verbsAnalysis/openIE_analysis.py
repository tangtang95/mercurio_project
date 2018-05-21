# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:47:18 2018

@author: Mattia
"""

from stanfordcorenlp import StanfordCoreNLP
from bs4 import BeautifulSoup
import re
from utilities import functions as fu

def split_article(article):
    # Split the content in different sentences
    delimiters = ".","!","?"
    regexPattern = "|".join(map(re.escape, delimiters))
    list_of_phrase = re.split(regexPattern, article)
    
    new_list = []
    for phrase in list_of_phrase:
        new_phrase = phrase
        new_list.append(new_phrase)
    return new_list        

def parse_openie_xml(xml):
    '''
    Given an xml containing a certain word, returns the triple.
    '''
    triple_save = ""
    try:
        soup = BeautifulSoup(xml, "lxml")
        list_of_solutions = soup.find("openie")
        for triple in list_of_solutions.find_all("triple"):
            if triple.get("confidence") == "1.000":
                for text in triple.find_all("text"):
                    triple_save = triple_save + text.string + " "
                if len(triple_save.split()) == 3:
                    return triple_save
                else:
                    triple_save = ""
        return ""        
    except Exception as err:
        return ""

def do_openie_analysis(list_of_phrase):
    with StanfordCoreNLP('http://localhost', port=9001, memory='4g') as nlp:   
        props = {'annotators': 'openie','pipelineLanguage':'en','outputFormat':'xml'}
    
        results = []
        for phrase in list_of_phrase:
            results.append(fu.get_lemmatized_text(parse_openie_xml(nlp.annotate(phrase, properties = props))))
            nlp.close()
        return results
    