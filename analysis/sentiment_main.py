# -*- coding: utf-8 -*-
import sys
from sentiment import sentiment_function as sf
from utilities import articlesDAO as dao
from utilities.database import Database
from utilities import functions as fu
from stanfordcorenlp import StanfordCoreNLP

def main():
    try:
        db = Database()
        db.open_connection()
        analyzed_dao = dao.ArticleAnalyzedDAO(db.get_database())
        result = analyzed_dao.getArticlesByNewsPaper(sys.argv[1])        
        vocabulary = fu.getVocabulary()
        with StanfordCoreNLP('http://localhost', port=9001, memory='4g') as nlp:
            for row in result:
                sentiment = sf.analyze_article(row[7], vocabulary, nlp)
                print("id: " + row[0])
                print("sentiment: " sentiment)
                analyzed_dao.updateNewsSentiment(row[0], sentiment)
    except Exception as err:
        raise Exception(err)
    finally:
        db.close_connection()
        
if __name__ == "__main__":
    main()
            