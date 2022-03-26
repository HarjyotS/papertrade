from logging import exception
import sqlite3


def register(email, id, password):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\auth\\maindb\\data.db"
    )
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
