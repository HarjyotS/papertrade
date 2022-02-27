from logging import exception
import sqlite3


def login(username, password):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\utils\\maindb\\data.db"
    )
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id =?", (username.lower(),))
        data = cur.fetchone()
        print(data)
        con.commit()
        con.close()
        if data is None:
            return False
        elif data[2] == password:

            return True
    except exception as e:
        print(e)
        con.close()
        return False


def checktok(username):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\utils\\maindb\\tokens.db"
    )
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tokens WHERE id =?", (username.lower(),))
        data = cur.fetchone()
        print(data)
        con.commit()
        con.close()
        if data is None:
            return False
        else:
            return
    except exception() as e:
        print(e)
        con.close()
        return False


login("ckm", "123")
