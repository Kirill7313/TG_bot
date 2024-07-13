import sqlite3

def auth():
    con = sqlite3.connect('bot_db.db')
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
def insert(bheader, bdate, btime, bdesc):
    con = sqlite3.connect('bot_db.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Events (header, date, time, desc) VALUES ('{bheader}', '{bdate}', '{btime}', '{bdesc}');")
    con.commit()