#!/usr/bin/python

import sys
import traceback
from coreference import coreference
from utilities import articlesDAO as dao
from utilities.database import Database
from utilities import functions
import MySQLdb

NUMBER_OF_PHRASE = 5

def main():
    '''
    Need to pass the newspaper as first argument
    '''
    try:
        db = Database()
        db.open_connection()
        full_articles_dao = dao.FullArticleDAO(db.get_database())
        result = full_articles_dao.getArticlesByNewsPaper(sys.argv[1])
        analyzed_dao = dao.ArticleAnalyzedDAO(db.get_database())
        for row in result:
            try:
                print(">> Analyzing...row with title: {0}".format(row[2]))
                print(">> Analyzing text size: {0}".format(len(row[5])))
                if(len(row[5]) > 0):
                    phrases = row[5].split('. ')
                    coref_content = ""
                    bigger_phrase = ""
                    i = 0
                    for phrase in phrases:
                        if i < NUMBER_OF_PHRASE:
                            bigger_phrase = bigger_phrase + phrase + ". "
                        if i == NUMBER_OF_PHRASE - 1:
                            #print(">> Phrase: {0}".format(bigger_phrase))
                            new_phrase = coreference.getCoreferencedText(bigger_phrase)
                            coref_content = coref_content + new_phrase
                            #print(">> Coref phrase: {0}".format(new_phrase))
                            i = 0
                            bigger_phrase = ""
                        i = i + 1
                    if i > 0:
                        #print(">> Phrase: {0}".format(bigger_phrase))
                        new_phrase = coreference.getCoreferencedText(bigger_phrase)
                        coref_content = coref_content + new_phrase
                        #print(">> Coref phrase: {0}".format(new_phrase))
                    print(">> Coref: " + coref_content)
                    lemma_content = functions.get_lemmatized_text(row[5])
                    analyzed_dao.insertNewsAnalyzed(row, coref_content, lemma_content)
                    print(">> News inserted")
                else:
                    print(">> empty string skipped")
            except Exception as err:  
                traceback.print_exc()
    except MySQLdb.Error as err:
        print(err)
    finally:
        db.close_connection()
    

if __name__ == "__main__":
    main()