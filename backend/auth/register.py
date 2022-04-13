from logging import exception
import sqlite3
import os

def register(email, id, password):
    path = f"{os.getcwd()}/auth/maindb/data.db"
    print(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    try:
        cur.execute(
            """INSERT INTO users (email, id, password)
                VALUES (?, ?, ?)""",
            (email, id.lower(), password),
        )
        con.commit()
        con.close()
        return True
    except exception as e:
        print(e)
        con.close()
        return False
