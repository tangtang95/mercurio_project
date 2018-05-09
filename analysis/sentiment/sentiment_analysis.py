# -*- coding: utf-8 -*-
from stanfordcorenlp import StanfordCoreNLP
import utilities.functions as fu
import utilities.articlesDAO as dao
import sentiment_function as sfu

# Initiliaze core element
nlp = StanfordCoreNLP(r'C:\Users\User.LAPTOP-FG37H74P\Desktop\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27')
keywords = fu.getKeywords()
full_articles_dao = dao.FullArticleDAO()
partial_articles_dao = dao.PartialArticleDAO()

#Retriving data
full_articles_dao.open_connection()
full_articles = full_articles_dao.getArticlesFromACertainDate()
full_articles_dao.close_connection()
partial_articles_dao.open_connection()
partial_articles = partial_articles_dao.getArticlesFromACertainDate()
partial_articles_dao.close_connection()


# Loop through DB content and
result = sfu.analyze_article("", keywords, nlp)

# Write result in DB


