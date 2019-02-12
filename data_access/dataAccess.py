import sqlite3

class DataAccess:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('resource/mytunes.sqlite')
            self.cursor = self.connection.cursor()
            self.__create_database()
        except:
            print('Failed to connect to database')

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def query(self, statement, values):
        self.cursor.execute(statement, values)
        return self.cursor.fetchone()

    def insert(self, statement, values):
        self.cursor.execute(statement, values)

    def commit(self):
        self.connection.commit()

    def __create_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS ARTIST;")
        self.cursor.execute("DROP TABLE IF EXISTS GENRE;")
        self.cursor.execute("DROP TABLE IF EXISTS ALBUM;")
        self.cursor.execute("DROP TABLE IF EXISTS TRACK;")


        self.cursor.execute('''CREATE TABLE ARTIST (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name TEXT UNIQUE);''')

        self.cursor.execute('''CREATE TABLE GENRE (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name TEXT UNIQUE)''')

        self.cursor.execute('''CREATE TABLE ALBUM (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ARTIST_ID INTEGER,
            title TEXT UNIQUE);''')

        self.cursor.execute('''CREATE TABLE TRACK (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            TITLE TEXT UNIQUE,
            ALBUM_ID INTEGER,
            GENRE_ID INTEGER,
            LEN INTEGER,
            RATING INTEGER,
            COUNT INTEGER);
            ''')
