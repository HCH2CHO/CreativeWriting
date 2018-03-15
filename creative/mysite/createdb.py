import sqlite3
conn=sqlite3.connect('db.sqlite3')
cur=conn.cursor()
cur.execute('''
CREATE TABLE if not exists history(
        id  TEXT  PRIMARY KEY,
        user TEXT,
        readinglist TEXT)
''')
conn.commit()
conn.close()

conn=sqlite3.connect('db.sqlite3')
cur=conn.cursor()
cur.execute('''
CREATE TABLE if not exists fiction(
        id  TEXT  PRIMARY KEY,
        words INT,
        wordfre TEXT,
        sl FLOAT,
        wl FLOAT,
        RE FLOAT,
        TFIDF TEXT,
        reArticle TEXT)
''')
conn.commit()
conn.close()