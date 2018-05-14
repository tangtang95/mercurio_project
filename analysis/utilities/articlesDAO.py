# -*- coding: utf-8 -*-
import MySQLdb

class ArticleDAO():
    def __init__(self, ip = '127.0.0.1', port = 3306, user = 'root',
                 password = 'mamma93', db = 'mercurio'):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        
    def open_connection(self):
        try:
            self.database = MySQLdb.connect(user = self.user, passwd = self.password, host = self.ip, port = self.port, db = self.db)
            self.database.set_character_set('utf8')
        except Exception as err:
            raise Exception(err)    

    def close_connection(self):
        self.database.close()
    
    def get_database(self):
        return self.database

class PartialArticleDAO(ArticleDAO):
    table = 'articles_en_partial'
    
    def getArticlesByCompanyInTitle(self, companies):
        '''
        Returns a list of articles that mention at least one company presents in
        company.
        '''
        try:
            where_clause = ""
            for i in range(0, len(companies)):
                if i < len(companies)-1:
                    where_clause = where_clause + "(Title LIKE %" + str(companies[i]) + "%) or "
                else:
                    where_clause = where_clause + "(Title LIKE %" + str(companies[i]) +"%)"
                    
                
            query = "SELECT * FROM %s WHERE " + where_clause
            cursor = self.database.cursor()
            return cursor.execute(query, [self.table])
        except Exception as err:
            raise Exception(err)
    
    def getArticlesByNewsPaper(self, newspaper):
        '''
        Returns every articles published by a certain source
        '''
        try:
            query = "SELECT * FROM %s WHERE Newspaper = %s"
            cursor = self.database.cursor()
            return cursor.execute(query, [self.table, newspaper])
        except Exception as err:
            raise Exception(err)

    def getArticlesFromACertainDate(self, date = None):
        '''
        Returns a list of articles starting from a specified date.
        Date must be given in format "Year-Month-Day".
        If date is None, all the articles are retrieved
        '''
        try:
            cursor = self.database.cursor()
            if date == None:
                query = "SELECT * FROM %s"
                return cursor.execute(query, [self.table])
            else:
                query = "SELECT * FROM %s WHERE date > %s"
                return cursor.execute(query, [self.table, date])
        except Exception as err:
            raise Exception(err)

class FullArticleDAO(PartialArticleDAO):
    table = 'articles_en_full'
    
    def getArticlesByKeyword(self, keywords):
        '''
        Returns a list of articles based on a list of keywords: each article
        matches at least a keyword in the tags field.
        '''
        try:
            where_clause = ""
            for i in range(0, len(keywords)):
                if i < len(keywords)-1:
                    where_clause = where_clause + "(Tags LIKE %" + str(keywords[i]) + "%) or "
                else:
                    where_clause = where_clause + "(Tags LIKE %" + str(keywords[i]) +"%)"
                    
            
            query = "SELECT * from %s WHERE " + where_clause
            cursor = self.database.cursor()
            return cursor.execute(query, [self.table])
        except Exception as err:
            raise Exception(err)