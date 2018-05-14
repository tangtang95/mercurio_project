import MySQLdb

class Database():

    def __init__(self, ip = '127.0.0.1', port = 3306, user = 'root',
                 password = 'mamma93', db_name = 'mercurio'):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        
    def open_connection(self):
        try:
            self.database = MySQLdb.connect(user = self.user, passwd = self.password,
                                            host = self.ip, port = self.port, db = self.db_name)
            self.database.set_character_set('utf8')
        except Exception as err:
            raise Exception(err)    

    def close_connection(self):
        self.database.close()
    
    def get_database(self):
        return self.database

