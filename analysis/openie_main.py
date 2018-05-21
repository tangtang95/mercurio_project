# -*- coding: utf-8 -*-
"""
Created on Mon May 14 14:49:40 2018

@author: Mattia
"""

import sys
from verbsAnalysis import openIE_analysis as IE
from utilities import functions as fu
from utilities import articlesDAO as dao
from utilities.database import Database

def main():
    '''
    Need to pass the newspaper as first argument
    '''
    table = 'openie_reports'
    
    try:
        db = Database()
        db.open_connection()
        full_articles_dao = dao.FullArticleDAO(db.get_database())
        list_of_news = full_articles_dao.getArticlesByNewsPaper(sys.argv[1])
    except Exception as err:
        print(err)
    for news in list_of_news:
        content = IE.do_openie_analysis(IE.split_article(news['content']))
        if content != None:
            insertNewsAnalyzedOnDatabase(db.get_database, content)
    
    cursor = db.cursor()        
    query = "SELECT subject FROM %s"
    list_of_subjects = cursor.execute(query, [table])
    print("Subjects: "+ list_of_subjects)
    subject = input("Choose a subject to analize: ")
    if subject in list_of_subjects:
        print_verbs_analyis(db, subject)
    else:
        print("Error")
    
    db.close_connection()
        
def insertNewsAnalyzedOnDatabase(database, new_content):
    '''
    insert the news in the database
    '''
    table = 'openie_reports'
    query = 'INSERT INTO ' + table + '(id, subject, verb, directObject) VALUES (%s, %s, %s, %s,)'
    cursor = database.cursor()
    for string in new_content:
        temp = string.split()
        if temp[1] in fu.getVocabulary() or temp[2] in fu.getVocabulary():
            cursor.execute(query, [None, temp[0], temp[1], temp[2]])
    
def print_verbs_analyis(database, subject):
    '''
    
    '''
    cursor = database.cursor()
    table = 'openie_reports'
    for word in fu.getVocabulary(): 
        query = "SELECT * FROM %s WHERE verb = %s GROUPBY subject = %s"
        cursor.execute(query, [table, word, subject])
        if cursor.rowcount > 0:
            print("" + subject + "verb analyzed: " + word + "-> " + cursor.rowcount)
      
    
if __name__ == "__main__":
    main()