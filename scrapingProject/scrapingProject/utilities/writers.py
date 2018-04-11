from scrapingProject.items import NewsItem, BriefItem
import csv
import MySQLdb

class ItemWriter():
    
    def open_writer(self):
        raise NotImplementedError
    
    def close_writer(self):
        raise NotImplementedError
    
    def write_item(self, *args):
        raise NotImplementedError
        
class FileItemWriter(ItemWriter):
    
    filename = 'default.tsv'
    
    def __init__(self, filename, item):
        self.filename = filename
        self.item = item
        
    def open_writer(self):
        self.file = open(self.filename, 'w')
        self.newswriter = csv.writer(self.file, delimiter='\t')
        
    def close_writer(self):
        self.file.close()
        
    def write_item(self, item):
        if type(item) is type(self.item):
            if isinstance(item, NewsItem):
                self.newswriter.writerow([item['title'], item['author'], 
                                  item['date'], item['time'], item['content'], item['tags']])
            else:
                self.newswriter.writerow([item['title'], item['url'], item['date'],
                                          item['time']])
        else:
            raise Exception('the item you passed is different from Writer Item gotten from constructor')

class DBItemWriter(ItemWriter):
    
    def __init__(self, item, newspaper, ip = '127.0.0.1', port = 3306, user = 'root',
                 password = 'mamma93', db = 'mercurio'):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.item = item
        self.newspaper = newspaper
    
    def open_writer(self):
        try:
            self.database = MySQLdb.connect(user = self.user, passwd = self.password, host = self.ip, port = self.port, db = self.db)
            self.database.set_character_set('utf8')
        except Exception as err:
            raise Exception(err)
        
    def close_writer(self):
        self.database.close()
        
    def write_item(self, item):
        if type(item) is type(self.item):
            try:
                if isinstance(item, NewsItem):
                    query = 'INSERT INTO articles_en_full(id, date, time, title, newspaper, author, content, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    cursor = self.database.cursor()
                    cursor.execute(query, [None, item['date'], 
                                  item['time'], item['title'], self.newspaper, 
                                  item['author'], item['content'], item['tags']])
                    
                else:
                    query = 'INSERT INTO articles_en_partial(id, date, time, title, newspaper, url) VALUES (%s, %s, %s, %s, %s, %s)'
                    cursor = self.database.cursor()
                    cursor.execute(query, [None, item['date'], item['time'],
                                   item['title'], self.newspaper, item['url']])
                self.database.commit()
            except MySQLdb.Error as err:
                raise Exception(err)
        else:
            raise Exception('the item you passed is different from Writer Item gotten from constructor')
    
        
    