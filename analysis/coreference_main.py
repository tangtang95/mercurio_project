#!/usr/bin/python

import sys
from coreference import coreference
from utilities import articlesDAO
from utilities import database

def main():
    '''
    Need to pass the newspaper as first argument
    '''
    try:
        db = database.Database()
        db.open_connection()
        full_articles_dao = articlesDAO.FullArticleDAO(db)
        list_of_news = full_articles_dao.getArticlesByNewsPaper(sys.argv[1])
    except Exception as err:
        print(err)
    analyzed_dao = articlesDAO.ArticleAnalyzedDAO(db)
    for news in list_of_news:
        content = coreference.getCoreferencedText(news['content'])
        print("Coref: " + content)
        analyzed_dao.insertNewsAnalyzed(news, content)
    db.close_connection()
    

if __name__ == "__main__":
    main()