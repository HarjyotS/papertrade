import sqlite3 as sql

con = sql.connect(
    "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\auth\\maindb\\userdata.db"
)
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY UNIQUE,
                holdings TEXT,
                transactions TEXT,
                watchlist TEXT,
                cash INTEGER);
            """
)
con.commit()
con.close()
