# -*- coding: utf-8 -*-
import sys
import traceback
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
                sentiment_neutral_strategy = sf.analyze_article(row[7], vocabulary, nlp, row[3], 1)
                sentiment_none_neutral_strategy = sf.analyze_article(row[7], vocabulary, nlp, row[3], 2)
                sentiment_summarize_strategy = sf.analyze_article(row[8], vocabulary, nlp, row[3], 3)
                print("id: " + str(row[0]))
                print("title: " + str(row[3]))
                print("sentiment1: " + sentiment_neutral_strategy)
                print("sentiment2: " + sentiment_none_neutral_strategy)
                print("sentiment3: " + sentiment_summarize_strategy)
                analyzed_dao.updateNewsSentimentStrategy1(row[0], sentiment_neutral_strategy)
                analyzed_dao.updateNewsSentimentStrategyNoNeutral(row[0], sentiment_none_neutral_strategy)
                analyzed_dao.updateNewsSentimentStrategySummarized(row[0], sentiment_summarize_strategy)
    except Exception as err:
        traceback.print_exc()
        raise Exception(err)
    finally:
        db.close_connection()
        
if __name__ == "__main__":
    main()
            