from stanfordcorenlp import StanfordCoreNLP
from bs4 import BeautifulSoup
import re

def getKeywords():
    '''
    Returns a list of financial keywords
    '''
    return read_file_per_line("resources/keywords.txt")

def getVocabulary():
    '''
    Returns a list of financial keywords
    '''
    return read_file_per_line("resources/lemmatized_vocabulary.txt")
    
def getCompanies():
    ''' 
    Returns a list of companies
    '''
    return read_file_per_line("../resources/companies.txt")
    
def read_file_per_line(file_path):
    '''
    Reads a file line by line, saving each line in a list.
    Returns the list.
    '''
    file = open(file_path, "r")
    keywords = []
    for line in file:
        if (line not in keywords):
            keywords.append(line)
    file.close()    
    return keywords
    
def write_file_per_line(file_path, toWriteList):
    '''
    Writes a list line per line in a specified file
    '''
    file = open(file_path, "w")
    for word in toWriteList:
        file.write(word)
        file.write("\n")
    file.close()
    
def lemmatize_file(file_path_in, file_path_out):
    '''
    Given an input file written per line and an output file, lemmatizes
    each word of the input file and write lemmas in output file.
    '''
    with StanfordCoreNLP('http://localhost', port=9001, memory='4g') as nlp:
        props = {'annotators': 'lemma','pipelineLanguage':'en','outputFormat':'xml'}    
        words = read_file_per_line(file_path_in)
        lemmatized_words = []
        for word in words:
            lemma = ""
            word = word.split(" ")
            for w in word:
                if w != " ":
                    xml = nlp.annotate(w, properties=props)
                    if lemma != "":
                        lemma = lemma+" "+parse_lemma_xml(xml)
                    else:
                        lemma = parse_lemma_xml(xml)
            lemmatized_words.append(lemma)
        write_file_per_line(file_path_out, lemmatized_words)
    
def get_lemmatized_complete_text(text):
    '''
    Given a string of text, lemmatizes each word and return the lemmatized text
    '''
    with StanfordCoreNLP('http://localhost', port=9001, memory='4g') as nlp:
        props = {'annotators': 'lemma','pipelineLanguage':'en','outputFormat':'xml'} 
        delimiters = ". ","!","?"
        regexPattern ="|".join(map(re.escape, delimiters))
        phrases = re.split(regexPattern, text)
        lemmatized_phrase = []
        for phrase in phrases:
            if len(text) <= 1:
                break
            words = phrase.split(" ")
            lemmatized_words = []
            for word in words:
                if word != "":
                    xml = nlp.annotate(word, properties=props)
                    lemma = parse_lemma_xml(xml)
                    lemmatized_words.append(lemma)
            si = text.find(phrase)
            lemmatized_phrase.append(' '.join(lemmatized_words)+text[len(phrase)+si:len(phrase)+int(si+1)])
            text = text[si + len(phrase): ]
    return ' '.join(lemmatized_phrase)
    
    
def parse_sentiment_xml(xml):
    '''
    Given an xml representing the result of corenlp sentiment annotator used
    on a sentence, returns the sentiment
    '''
    try:
        soup = BeautifulSoup(xml)
        return soup.find("sentiment").string
    except Exception as err:
        return "neutral"

def parse_lemma_xml(xml):
    '''
    Given an xml representing the result of corenlp lemma annotator used on a 
    single word, returns the lemma.
    '''
    try:
        soup = BeautifulSoup(xml, "html5lib")
        return soup.find("lemma").string
    except Exception as err:
        return ""              
    
def give_article_from_server():
    #TODO
    return "Keith is the Chief Investment Strategist for Money Map Press. A seasoned market analyst and professional trader with more than 30 years of global experience, Keith is one of very few experts to correctly see both the dot.bomb crisis and the ongoing financial crisis coming ahead of time - and one of even fewer to help millions of investors around the world successfully navigate them both. Forbes.com recently hailed him as a Market Visionary. He is a regular on FOX Business, CNBC, and CNBC Asia, and his observations have been featured in Bloomberg, The Wall Street Journal, WIRED, Forbes, and MarketWatch. Keith has been leading The Money Map Report since 2008, our flagship newsletter with 80,000+ members. He's also the editor of the High Velocity Profits trading service. In his new weekly Total Wealth, Keith has taken everything he's learned over a notable career and distilled it down to just three steps for individual investors. Sign up is free at totalwealthresearch.com. Keith holds a BS in management and finance from Skidmore College and an MS in international finance (with a focus on Japanese business science) from Chaminade University. He regularly travels the world in search of investment opportunities others don't yet see or understand."

def write_on_db(string):
    #TODO
    file_path = r"C:\Users\user\Documents\GitHub\mercurio_project\analysis\resources\openIE_reports.txt"
    
    if string != "":
        file = open(file_path,"a")
        file.write(string + "\n")
        file.close()

