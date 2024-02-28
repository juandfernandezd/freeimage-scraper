import sqlite3


def init_db():
    connection = sqlite3.connect('images.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images 
                      (id INTEGER PRIMARY KEY, url TEXT)''')
    connection.commit()

    return connection, cursor


def insert_images(conn, cursor, images_urls):
    query = 'INSERT INTO images (url) VALUES (?)'
    cursor.executemany(query, images_urls)
    conn.commit()
