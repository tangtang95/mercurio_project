# -*- coding: utf-8 -*-

from stanfordcorenlp import StanfordCoreNLP
from bs4 import BeautifulSoup

def getCoreferencedText(text):
    '''
    Return the text with the coreferenced object changed with the 
    representative\n
    - text: a string of text to analyze
    '''
    with StanfordCoreNLP(r'/Users/tangtang.zhou/Downloads/stanford-corenlp-full-2018-02-27') as nlp:
        props = {'annotators': 'coref', 'pipelineLanguage': 'en', 'outputFormat': 'xml'}
        xml_text = nlp.annotate(text, properties = props)
        soup = BeautifulSoup(xml_text, "html5lib")
        sentences = soup.find("sentences")
        list_of_mentions = soup.find("coreference").find_all("mention")
        for mention in list_of_mentions:
            if mention.has_attr('representative'):
                representative = mention
            else:
                tokens = getTokensFromSentenceByWord(sentences, 
                                           mention.find("sentence").text,
                                           mention.find("start").text,
                                           mention.find("end").text)
                done = False
                for token in tokens:
                    if done == False:
                        if token.find("pos").text == "PRP$":
                            token.find("word").string.replace_with(representative.find("text").text + "\'s")
                        else:
                            token.find("word").string.replace_with(representative.find("text").text)
                        done = True
                    else:
                        token.extract()
        return getTextFromSentences(sentences)
                
                    
        
def getTokensFromSentenceByWord(sentences, idSentence, startId, endId):
    '''
    Return a list of bs4.element object representing the a tag token that contains
    everything about a word\n
    - sentences: a bs4.element xml object of the tag sentences
    - idSentence: a string representing the id of the sentence
    - startId: the start id of the tokens
    - endId; the end id of the tokens
    '''
    tokens_element = sentences.find("sentence", {"id" : idSentence}).find("tokens")
    tokens = []
    for i in range(int(startId), int(endId)):
        tokens.append(tokens_element.find("token", {"id" : str(i)}))
    return tokens


def getTextFromSentences(sentences):
    '''
    Return a reconstructed text from a bs4.element xml object of the tag sentences\n
    - sentences: a bs4.element xml object of the tag sentences
    '''
    text = ""
    list_of_sentence = sentences.find_all("sentence")
    for sentence in list_of_sentence:
        list_of_tokens = sentence.find_all("token")
        for token in list_of_tokens:
            text = text + token.find("word").text + " "
    return text