import sqlite3
import json

class Database:
    TABLE = '''CREATE TABLE IF NOT EXISTS property(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL UNIQUE,
        price INTEGER NOT NULL);

        CREATE TABLE IF NOT EXISTS property_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        bed TEXT, bath TEXT, sqft TEXT, type TEXT);
        '''


    def __init__ (self):
        print('I am creating an object of class database')
        self.conn = sqlite3.connect('property.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.executescript(Database.TABLE)

    def insert(self, statement, params):
        self.cursor.execute(statement, params)
        self.conn.commit()

    def query(self, statement, params):
        self.cursor.execute(statement, params)
        row = self.cursor.fetchone()
        if row is None:
            print('There is nothing to return')
            return None

        return row

    def __del__(self):
        print('Destructor')
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
