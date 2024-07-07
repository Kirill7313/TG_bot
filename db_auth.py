import sqlite3

def auth(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    header TEXT,
    time TEXT,
    desc TEXT
    );
    ''')
    con.commit()
    con.close()
def ret_con(db):
    return sqlite3.connect(db)
def ret_cur(db):
    return sqlite3.connect(db).cursor()
sqlite3.connect('bot_db.db').cursor().execute('''INSERT INTO \'Events\' (date, header, time, desc) VALUES (\'2024-07-06\', "Sigmas", "15:00", "Sigmas description")''')