import sqlite3


def remade(kort):
    values=[]
    for i in range(len(kort)):
        v=[]
        for t in kort[i]:
            v.append(t)
        values.append(v)
    return values
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
def get_headers(day):
    con = sqlite3.connect('bot_db.db')
    cur = con.cursor()
    cur.execute(f"SELECT id,header FROM Events WHERE date = '{day}'")
    result = cur.fetchall()
    result=remade(result)
    if len(result)==0:
        return False
    else:
        return result
def get_info(id_):
    con = sqlite3.connect('bot_db.db')
    cur = con.cursor()
    cur.execute(f"SELECT header,date,time,desc FROM Events WHERE id = '{id_}'")
    result = cur.fetchall()
    result=remade(result)
    return result[0]


# cur.execute('''INSERT INTO \'Events\' (date, header, time, desc) VALUES (\'2024-07-11\', "Sigmas", "15:00", "Sigmas description")''')
# con.commit()
#get_header('2024-07-06')        

