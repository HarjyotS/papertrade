import sqlite3 as sql

con = sql.connect("./utils/maindb/tokens.db")
cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS tokens (
                id TEXT PRIMARY KEY UNIQUE,
                token TEXT)
            """
)
con.commit()
con.close()
