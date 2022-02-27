import sqlite3 as sql

con = sql.connect("./utils/maindb/data.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY UNIQUE,
                password TEXT,
                email TEXT UNIQUE)
            """
)
con.commit()
con.close()
