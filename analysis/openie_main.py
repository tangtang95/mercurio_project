# -*- coding: utf-8 -*-
"""
Created on Mon May 14 14:49:40 2018

@author: Mattia
"""

import sys
from verbsAnalysis import openIE_analysis as IE
from utilities import functions as fu
from utilities import articlesDAO

def main():
    '''
    Need to pass the newspaper as first argument
    '''
    try:
        db = articlesDAO.CoreferencesArticleDAO()
        list_of_news = db.getArticlesByNewsPaper(sys.argv[1])
    except Exception as err:
        print(err)
    for news in list_of_news:
        content = IE.do_openie_analysis(IE.split_article(news['content']))
        if content != None:
            insertNewsAnalyzedOnDatabase(db.get_database, content)
    db.close_connection()
        
def insertNewsAnalyzedOnDatabase(database, new_content):
    '''
    insert the news in the database
    '''
    table = 'openIE_reports'
    query = 'INSERT INTO ' + table + '(id, subject, verb, direct_object) VALUES (%s, %s, %s, %s,)'
    cursor = database.cursor()
    for string in new_content:
        temp = string.split()
        if temp[1] in fu.getVocabulary() or temp[2] in fu.getVocabulary():
            cursor.execute(query, [None, temp[0], temp[1], temp[2]])
    

if __name__ == "__main__":
    main()