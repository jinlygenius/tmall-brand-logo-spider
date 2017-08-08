import sqlite3
from datetime import datetime
import os
con = None


class TmallBrandsDB(object):

    def __init__(self):
        self.setupDBCon()
        self.initTables()

    def process_item(self, item):
        self.storeInDb(item)
        return item

    def setupDBCon(self):
        # self.con = sqlite3.connect('./test.db') #Change this to your own directory
        self.con = sqlite3.connect(os.getcwd() + '/tmall_brands.db')
        self.cur = self.con.cursor()
     
    def initTables(self):
        try:
            self.createTable()
        except:
            pass
     
    def createTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Tmall(id INTEGER PRIMARY KEY NOT NULL, keyword TEXT, image_urls TEXT, created_time DATETIME )")

    def dropTable(self):
        #drop table if it exists
        self.cur.execute("DROP TABLE IF EXISTS Tmall")

    def storeInDb(self, item):
        image_urls = item.get('image_urls','')
        if image_urls:
            image_urls = image_urls
        self.cur.execute("INSERT INTO Tmall(keyword, image_urls, created_time) VALUES( ?, ?, ?)", \
        ( \
        item.get('keyword',''),
        image_urls,
        datetime.now()
        ))
        print('------------------------')
        print('Data Stored in Database')
        print('------------------------')
        self.con.commit()

    def closeDB(self):
        self.con.close()
         
    def __del__(self):
        self.closeDB()