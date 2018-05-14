#!/usr/bin/python

import sys
from coreference import coreference
from utilities import articlesDAO

def main():
    '''
    Need to pass the newspaper as first argument
    '''
    try:
        db = articlesDAO.FullArticleDAO()
        list_of_news = db.getArticlesByNewsPaper(sys.argv[1])
    except Exception as err:
        print(err)
    for news in list_of_news:
        content = coreference.getCoreferencedText(news['content'])
        print("Coref: " + content)
        content = coreference.getLemmatizedText(content)
        print("Lemma: " + content)
        insertNewsAnalyzedOnDatabase(db.get_database, news, content)
    db.close_connection()
        
def insertNewsAnalyzedOnDatabase(database, news, new_content):
    '''
    insert the news in the database
    '''
    table = 'articles_en_analyzed'
    query = 'INSERT INTO '+ table + '(id, date, time, title, newspaper, author, content, tags, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor = database.cursor()
    cursor.execute(query, [None, news['date'], news['time'], news['title'], news['newspaper'], 
                           news['author'], new_content, news['tags'], None])
    

if __name__ == "__main__":
    main()