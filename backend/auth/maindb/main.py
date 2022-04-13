# open data.db and print all values of the table inside

import sqlite3


def printall():
    conn = sqlite3.connect("/papertrade/auth/maindb/data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    for row in c.fetchall():
        print(row)
    conn.close()


printall()
