

class ArticleDAO():
    def __init__(self, database):
        '''
        Constructor.\n
        - database: database object got from MySQLdb.connect
        '''
        self.database = database

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
                    
                
            query = "SELECT DISTINCT date,time,title,newspaper,author,content,tags  FROM {0} WHERE ".format(self.table) + where_clause + ";"
            cursor = self.database.cursor()
            cursor.execute(query)
            return cursor
        except Exception as err:
            raise Exception(err)
    
    def getArticlesByNewsPaper(self, newspaper):
        '''
        Returns every articles published by a certain source
        '''
        try:
            query = "SELECT DISTINCT date,time,title,newspaper,author,content,tags FROM {0} WHERE Newspaper = %s;".format(self.table)
            cursor = self.database.cursor()
            cursor.execute(query, [newspaper])
            return cursor
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
                query = "SELECT DISTINCT date,time,title,newspaper,author,content,tags FROM {0};".format(self.table)
                cursor.execute(query)
            else:
                query = "SELECT DISTINCT date,time,title,newspaper,author,content,tags FROM {0} WHERE date > %s;".format(self.table)
                cursor.execute(query, [date])
            return cursor
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
                    
            
            query = "SELECT DISTINCT date,time,title,newspaper,author,content,tags from {0} WHERE ".format(self.table) + where_clause + ";"
            cursor = self.database.cursor()
            cursor.execute(query)
            return cursor
        except Exception as err:
            raise Exception(err)
            
            

class ArticleAnalyzedDAO(FullArticleDAO):
    table = 'articles_en_analyzed'
    
    def insertNewsAnalyzed(self, news, coref_content, lemma_content):
        '''
        Insert the news in the database
        '''
        try:
            query = 'INSERT INTO '+ self.table + ' VALUES (%s , %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            cursor = self.database.cursor()
            cursor.execute(query,[None, news[0], news[1], news[2], news[3], news[4], coref_content, lemma_content, news[6], None])
            self.database.commit()
        except Exception as err:
            raise Exception(err)
        
    def updateNewsSentiment(self, news_id, sentiment):
        '''
        Update the field sentiment of a specified news
        '''
        try:
            query = 'UPDATE ' + self.table + ' SET sentiment = %s  WHERE articledId = %d ;'
            cursor = self.database.cursor()
            cursor.execute(query, [sentiment, int(news_id)])
            self.database.commit()
        except Exception as err:
            raise Exception(err)
            
    
    def getArticlesByNewsPaper(self, newspaper):
        '''
        Returns every articles published by a certain source
        '''
        try:
            query = "SELECT * FROM " + self.table + " WHERE Newspaper = %s"
            cursor = self.database.cursor()
            cursor.execute(query, [newspaper])
            return cursor
        except Exception as err:
            raise Exception(err) 
