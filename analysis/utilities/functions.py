from stanfordcorenlp import StanfordCoreNLP
from bs4 import BeautifulSoup

def getKeywords():
    '''
    Returns a list of financial keywords
    '''
    return read_file_per_line("resources/keywords.txt")
    
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
    nlp = StanfordCoreNLP(r'C:\Users\User.LAPTOP-FG37H74P\Desktop\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27')
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
        soup = BeautifulSoup(xml)
        return soup.find("lemma").string
    except Exception as err:
        return ""              
    
def give_article_from_server():
    #TODO
    return ""

def write_on_db(string):
    #TODO
    if string != "":
        print(string)

