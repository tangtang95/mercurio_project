# -*- coding: utf-8 -*-
import re as re
from stanfordcorenlp import StanfordCoreNLP
import utilities.functions as fu
import sentiment.summarization as summarize

STRATEGY_NEUTRAL_VOCABULARY = 1
STRATEGY_NO_NETRUAL_VOCABULARY = 2
STRATEGY_SUMMARIZATION = 3

def analyze_article(content, financial_vocabulary, nlp_analyzer, title, strategy):
    '''
    Given an article made of more sentences, it analyzes the sentiment of the 
    article by inspecting each sentence and by weighting them on different criterias
    specified with strategy.
  
        -The phrase can contains more words from a defined financial vocabulary list.
        Counting this terms helps in assigning an amplified weight to the sentences.
        Neutral values are here significant. (strategy = 1)
    
        -Same of the point mentioned above, but netruals are ignored. (strategy = 2)

        -Weights are assigned analyzing a summarization of the article. (strategy = 3)

    This returns a string that can be: 'positive', 'very positive', 'very negative',
    'negative' or 'neutral'.
    '''
    # Setup
    props = {'annotators': 'lemma','pipelineLanguage':'en','outputFormat':'xml'}
    sentiments = {'positive': 0, 'very positive': 0, 'neutral': 0, 'negative':0, 'very negative':0}
    sentences = []
    
    if strategy == STRATEGY_SUMMARIZATION:
        content = summarize.Summarize(title, content)
    
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

    if strategy == STRATEGY_NEUTRAL_VOCABULARY or strategy == STRATEGY_SUMMARIZATION:    
        return get_sentiment(get_article_weight(sentiments))
    elif strategy == STRATEGY_NO_NETRUAL_VOCABULARY:
        return get_sentiment(get_article_weight_no_neutral(sentiments))

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
    result = ["very negative", "negative", "neutral", "positive", "very positive"]
    interval = 2 / float(len(result))
    
    for i in range(1,5):
        if(article_w <= -1 + i * interval):
            return result[i-1]
    return result[4]


def get_article_weight_no_neutral(sentiments):
    '''
    Returns the weight of an article as a weighted medium based on the following fact:
    neutral weights 0, positive and negative 0.4 and -0.4, very positive and very
    negative 0.8 and -0.8. Netrual are not counted in the division process. 
    '''
    wsum = sentiments['very negative'] * (-0.8)
    wsum = wsum + sentiments['negative'] * (-0.4)
    wsum = wsum + sentiments['positive'] * 0.4
    wsum = wsum + sentiments['very positive'] * 0.8
    total = 0
    for key in sentiments:
        if key != 'neutral':
            total = total + sentiments[key]
    return wsum / float(total)

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
    return wsum / float(total)
    
    
    
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
            weight = weight + 0.1
    return weight
        
    

