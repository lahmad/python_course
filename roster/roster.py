import json
import sqlite3

def main():
    connection = sqlite3.connect('roster.sqlite')
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS COURSE;')
    cursor.execute('DROP TABLE IF EXISTS USER;')
    cursor.execute('DROP TABLE IF EXISTS MEMBER;')

    cursor.execute(''' CREATE TABLE USER (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE);''')

    cursor.execute(''' CREATE TABLE COURSE (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            title TEXT UNIQUE);''')

    cursor.execute(''' CREATE TABLE MEMBER (
            ROLE INTEGER,
            USER_ID INTEGER,
            COURSE_ID INTEGER,
            PRIMARY KEY(USER_ID, COURSE_ID)
            );''')

    file_handler = open('roster_data.json', 'r')

    if file_handler is None:
        print('cannot open file')

    message = json.load(file_handler)

    for item in message:
        name = item[0]
        course = item[1]
        role = item[2]

        cursor.execute('INSERT OR IGNORE INTO USER(name) VALUES(?)', (name,))
        cursor.execute('SELECT id from USER WHERE name = ?', (name,))
        user_id = cursor.fetchone()[0]

        cursor.execute('INSERT OR IGNORE INTO COURSE(title) VALUES(?)', (course,))
        cursor.execute('SELECT id FROM COURSE WHERE title = ?', (course,))
        course_id = cursor.fetchone()[0]

        cursor.execute('INSERT OR REPLACE INTO MEMBER(user_id, course_id, role) VALUES(?,?,?)', (user_id, course_id, role))
        connection.commit()

    connection.close()
    file_handler.close()


if __name__ == '__main__':
    main()
