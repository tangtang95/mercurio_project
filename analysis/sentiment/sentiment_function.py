# -*- coding: utf-8 -*-
import re as re
from stanfordcorenlp import StanfordCoreNLP
import utilities.functions as fu

def analyze_article(content, financial_vocabulary, nlp_analyzer):
    '''
    Given an article made of more sentences, it analyzes the sentiment of the 
    article by inspecting each sentence and by weighting them on a criteria
    based on the fact that the phrase can contains more words from a defined financial
    vocabulary list. 
    This returns a string that can be: 'positive', 'very positive', 'very negative',
    'negative' or 'neutral'.
    '''
    # Setup
    props = {'annotators': 'lemma','pipelineLanguage':'en','outputFormat':'xml'}
    sentiments = {'positive': 0, 'very positive': 0, 'neutral': 0, 'negative':0, 'very negative':0}
    sentences = []
    
    # Split the content in different sentences
    delimiters = ".","!","?"
    regexPattern ="|".join(map(re.escape, delimiters))
    s = re.split(regexPattern, content)
    for sentence in s:
        si = content.find(sentence)
        sentences.append(sentence+content[len(sentence)+si:len(sentence)+int(si+1)])
    
    # Analyze each sentence 
    for sentence in sentences:
        sentiment = fu.parse_sentiment_xml(nlp_analyzer.annotate(sentence, properties = props))
        sentiments[sentiment] = sentiments[sentiment] + get_sentence_weight(sentence, financial_vocabulary)
    return get_sentiment(get_article_weight(sentiments))
    
def get_sentiment(article_w):
    '''
    Takes as input a number ranging in [-1, 1] and returns the correct sentiment
    splitting this interval in 5 zones and associating each zone with a sentiment.
    - [-1, -0.6] is very negative
    - (-0.6, -0.2] is negative
    - (-0.2, +0.2] is neutral
    - (+0.2, 0.6] is positive
    - (0.6, 1] is very positive
    '''
    interval = 2 / 5
    result = ["very negative", "negative", "neutral", "positive", "very positive"]
    
    for i in range(1,5):
        if(article_w <= -1 + i * interval):
            return result[i-1]
    return result[4]

def get_article_weight(sentiments):
    '''
    Returns the weight of an article as a weighted medium based on the following fact:
    neutral weights 0, positive and negative 0.4 and -0.4, very positive and very
    negative 0.8 and -0.8.
    '''
    wsum = sentiments['very negative'] * (-0.8)
    wsum = wsum + sentiments['negative'] * (-0.4)
    wsum = wsum + sentiments['positive'] * 0.4
    wsum = wsum + sentiments['very positive'] * 0.8
    total = 0
    for key in sentiments:
        total = total + sentiments[key]
    return wsum / total
    
    
    
def get_sentence_weight(sentence, word_list):
    '''
    Returns the weight of the sentence.
    The actual policy in calculating the weight is the following:
    everytime that a word in word_list is present in the sentece, the weight 
    get increment by one.
    '''
    weight = 1
    for word in word_list:
        if word in sentence:
            weight = weight + 0.5
    return weight
        
    

