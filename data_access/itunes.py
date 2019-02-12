import sqlite3
import xml.etree.ElementTree as ET
from dataAccess import DataAccess

def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True

    return None

def main():

    # Create a database object
    data_access = DataAccess()

    root = ET.parse('resource/Library.xml')
    elements = root.findall('dict/dict/dict')
    print('Number of tracks: ', len(elements))

    for entry in elements:
        if lookup(entry, 'Track ID') is None: continue
        name = lookup(entry, 'Name')
        artist = lookup(entry, 'Artist')
        title = lookup(entry, 'Album')
        rating = lookup(entry, 'Rating')
        genre = lookup(entry, 'Genre')
        count = lookup(entry, 'Track Count')
        length = lookup(entry, 'Total Time')

        if name is None or artist is None or genre is None or title is None:
            continue

        print('Name : ', name)
        print('Artist: ', artist)
        print('Album: ', title)
        print('Rating: ', rating)
        print('Genre: ', genre)
        print('Count: ', count)
        print('Total time: ', length)


        # Populate the artist TABLE
        data_access.insert('INSERT OR IGNORE INTO ARTIST(name) VALUES(?);', (artist,))
        artist_rows = data_access.query('SELECT id  FROM ARTIST WHERE name = ?;', (artist,))
        artist_id = artist_rows[0]

        # Populate the genre TABLE
        data_access.insert('INSERT OR IGNORE INTO GENRE(name) VALUES(?);', (genre,))
        genre_rows = data_access.query('SELECT id FROM GENRE WHERE name = ?;', (genre,))
        genre_id = genre_rows[0]

        # Populate the album TABLE
        data_access.insert('INSERT OR IGNORE INTO ALBUM(title, artist_id) VALUES(?, ?)', (title, artist_id,))
        album_rows= data_access.query('SELECT id FROM ALBUM where title = ?', (title,))
        album_id = album_rows[0]

        # Populate the tracks
        data_access.insert('INSERT OR REPLACE INTO TRACK (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)',
            (title, album_id, genre_id, length, rating, count,))

        data_access.commit()












if __name__ == '__main__':
    main()
