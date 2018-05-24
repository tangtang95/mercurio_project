#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:40:35 2017

@author: Fabio
"""

from collections import Counter
from math import fabs
from re import split as regex_split, sub as regex_sub, UNICODE as REGEX_UNICODE

stopWords = set(["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldn't", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "just", "keep 	keeps", "kept", "kg", "km", "know", "known", "knows", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "que", "quickly", "quite", "qv", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "zero" ])

ideal = 20.0

def Summarize(title, text):
    summary = []
    sentences = split_sentences(text)
    
    #numero di frasi da tenere
    n = round((len(sentences)/4) -3)
    
    #rimuovo citazioni lunghe nella stessa frase
    delete_list = []
    for i in range(len(sentences)):
        if("«" in sentences[i] and "»" in sentences[i]):
            quotation_start = sentences[i].find('«')
            quotation_end = sentences[i].find('»')
            if(quotation_end - quotation_start > 35):
                delete_list.append(i)
    delete_list.sort(reverse=True)
    for i in delete_list:
        del sentences[i]

    #rimuovo citazioni lunghe su più frasi
    i = 0
    delete_list = []
    while i < len(sentences):
        if("«" in sentences[i] and "»" not in sentences[i]):
            delete_list.append(i)
            done = False
            i = i+1
            while(not done and i < len(sentences)):
                if("»" in sentences[i]):
                    delete_list.append(i)
                    done = True
                else:
                    delete_list.append(i)
                    i = i+1
        i = i+1
    delete_list.sort(reverse=True)
    for i in delete_list:
        del sentences[i]
                
    original_sentences = sentences[:]
    keys = keywords(text)
    titleWords = split_words(title)
    
    if len(sentences) <= n+3:
        return sentences
    
    #la prima, la seconda e l'ultima frase le rimuovo temporaneamente in quanto le prendo sempre 
    del sentences[0]
    del sentences[0]
    del sentences[-1]
    
    #score setences, and use the top n sentences
    ranks = score(sentences, titleWords, keys).most_common(n)
    for rank in ranks:
        summary.append(rank[0])
    
    tmp = []
    #aggiungo la prima e la seconda frase
    tmp.append(original_sentences[0])
    tmp.append(original_sentences[1])
    
    #riordino le frasi selezionate nell'ordine in cui erano nell'articolo
    k = len(original_sentences)-1    
    for i in range(2, k):
        if original_sentences[i] in summary:
            tmp.append(original_sentences[i])       
    #aggiungo l'ultima frase
    tmp.append(original_sentences[-1])     
    summary = tmp
    return summary



def score(sentences, titleWords, keywords):
    #score sentences based on different features
    senSize = len(sentences)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = split_words(s)
        titleFeature = title_score(titleWords, sentence)
        sentenceLength = length_score(sentence)
        sentencePosition = sentence_position(i+1, senSize)
        sbsFeature = sbs(sentence, keywords)
        dbsFeature = dbs(sentence, keywords)
        frequency = (sbsFeature + dbsFeature) / 2.0 * 10.0

        #se contiene numeri seguiti da milione/i, miliardo/i, %, euro
        numbers = 0
        if (any(char.isdigit() for char in s)):
            if("milion" in s or "miliard" in s or "euro" in s or "%" in s):
                numbers = 1.0
        
        #weighted average of scores from four categories
        totalScore = (titleFeature*1.5 + frequency*2.0 +
                      sentenceLength*1.0 + sentencePosition*1.0 + numbers*2.0) / 5.0
        ranks[s] = totalScore
    return ranks


def sbs(words, keywords):
    score = 0.0
    if len(words) == 0:
        return 0
    for word in words:
        if word in keywords:
            score += keywords[word]
    return (1.0 / fabs(len(words)) * score)/10.0


def dbs(words, keywords):
    if (len(words) == 0):
        return 0

    summ = 0
    first = []
    second = []

    for i, word in enumerate(words):
        if word in keywords:
            score = keywords[word]
            if first == []:
                first = [i, score]
            else:
                second = first
                first = [i, score]
                dif = first[0] - second[0]
                summ += (first[1]*second[1]) / (dif ** 2)

    # number of intersections
    k = len(set(keywords.keys()).intersection(set(words))) + 1
    return (1/(k*(k+1.0))*summ)


def split_words(text):
    #split a string into array of words
    try:
        text = regex_sub(r'[^\w ]', '', text, flags=REGEX_UNICODE)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        print("Error while splitting characters")
        return None


def keywords(text):
    """get the top 10 keywords and their frequency scores
    ignores blacklisted words in stopWords,
    counts the number of occurrences of each word
    """
    text = split_words(text)
    numWords = len(text)  # of words before removing blacklist words
    freq = Counter(x for x in text if x not in stopWords)

    minSize = min(10, len(freq))  # get first 10
    keywords = {x: y for x, y in freq.most_common(minSize)}  # recreate a dict

    for k in keywords:
        articleScore = keywords[k]*1.0 / numWords
        keywords[k] = articleScore * 1.5 + 1

    return keywords


def split_sentences(text):
    '''
    The regular expression matches all sentence ending punctuation and splits the string at those points.
    At this point in the code, the list looks like this ["Hello, world", "!" ... ]. The punctuation and all quotation marks
    are separated from the actual text. The first s_iter line turns each group of two items in the list into a tuple,
    excluding the last item in the list (the last item in the list does not need to have this performed on it). Then,
    the second s_iter line combines each tuple in the list into a single item and removes any whitespace at the beginning
    of the line. Now, the s_iter list is formatted correctly but it is missing the last item of the sentences list. The
    second to last line adds this item to the s_iter list and the last line returns the full list.
    '''
    
    sentences = regex_split(u'(?<![A-ZА-ЯЁ])([.!?]"?)(?=\s+\"?[A-ZА-ЯЁ])', text, flags=REGEX_UNICODE)
    s_iter = zip(*[iter(sentences[:-1])] * 2)
    s_iter = [''.join(map(str,y)).lstrip() for y in s_iter]
    s_iter.append(sentences[-1])
    return s_iter

def length_score(sentence):
    return 1 - fabs(ideal - len(sentence)) / ideal


def title_score(title, sentence):
    title = [x for x in title if x not in stopWords]
    count = 0.0
    for word in sentence:
        if (word not in stopWords and word in title):
            count += 1.0
            
    if len(title) == 0:
        return 0.0
        
    return count/len(title)

# abbiamo uniformato i pesi in quanto prendiamo gia di default prima, seconda e ultima frase
def sentence_position(i, size):
    """different sentence positions indicate different
    probability of being an important sentence"""
    normalized = i*1.0 / size
    if 0 < normalized <= 0.1:
        return 0.1
    elif 0.1 < normalized <= 0.2:
        return 0.1
    elif 0.2 < normalized <= 0.3:
        return 0.1
    elif 0.3 < normalized <= 0.4:
        return 0.1
    elif 0.4 < normalized <= 0.5:
        return 0.1
    elif 0.5 < normalized <= 0.6:
        return 0.1
    elif 0.6 < normalized <= 0.7:
        return 0.1
    elif 0.7 < normalized <= 0.8:
        return 0.1
    elif 0.8 < normalized <= 0.9:
        return 0.1
    elif 0.9 < normalized <= 1.0:
        return 0.1
    else:
        return 0
