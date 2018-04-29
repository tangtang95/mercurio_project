# -*- coding: utf-8 -*-
from stanfordcorenlp import StanfordCoreNLP
import utilities.functions as fu
import utilities.articlesDAO as dao

# Initiliaze core elements
nlp = StanfordCoreNLP(r'C:\Users\User.LAPTOP-FG37H74P\Desktop\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27')
sentiments = {'positive': 0, 'very positive': 0, 'neutral': 0, 'negative':0, 'very negative':0}
keywords = fu.getKeywords()
full_articles_dao = dao.FullArticleDAO()
partial_articles_dao = dao.PartialArticleDAO()
subjects = fu.getCompanies()

#Retriving data
full_articles_dao.open_connection()
full_articles = full_articles_dao.getArticlesFromACertainDate()
full_articles_dao.close_connection()
partial_articles_dao.open_connection()
partial_articles = partial_articles_dao.getArticlesFromACertainDate()
partial_articles_dao.close_connection()

# Identify subject: it must be in the title: how to distinguish it? Company name?
title = ""
article = ""

# Identify words from a list of financial words


# Analysis for each sentences, saving the value in an array

