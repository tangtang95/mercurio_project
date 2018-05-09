# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:47:18 2018

@author: Mattia
"""

from stanfordcorenlp import StanfordCoreNLP
import utilities.functions as fu
from bs4 import BeautifulSoup
import re

file_path = r"C:\Users\user\Documents\GitHub\mercurio_project\analysis\resources\openIE_reports.xml"

def do_coreferences(article):
    list_of_phrase = re.split(".|!|?|...")
    new_list = []
    for phrase in list_of_phrase:
        #TODO coreference
        new_phrase = phrase
        new_list.append(new_phrase)
    return new_list        

def parse_openie_xml(xml):
    '''
    Given an xml containing a certain word, returns the triple.
    '''
    try:
        soup = BeautifulSoup(xml)
        list_of_solutions = soup.openie
        for triple in list_of_solutions.find_all("triple"):
            if triple.get("confidence") == "1.000":
                triple_save = triple.string
                if len(triple_save.split()) == 3:
                    return triple_save           
    except Exception as err:
        return "" 

def do_openie_analysis(list_of_phrase):
    nlp = StanfordCoreNLP(r"C:\Program Files\Python36\stanford-corenlp-full-2018-02-27" + 
                      "\stanford-corenlp-full-2018-02-27")    
    props = {'annotators': 'openie','pipelineLanguage':'en','outputFormat':'xml'}
    
    for phrase in list_of_phrase:
        fu.write_on_db(parse_openie_xml(nlp.annotate(sentence, properties = props)))
    nlp.close()
    
    
sentence = "Richard buy the market."
article = fu.give_article_from_server()
do_openie_analysis(do_coreferences(sentence))



