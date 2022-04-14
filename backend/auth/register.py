from utils import exceptions

import sqlite3
import os
from contextlib import closing


def register(*, email, username, password):
    path = f"{os.getcwd()}/maindb/data.db"
    with closing(sqlite3.connect(path, isolation_level=None)) as con:
        with closing(con.cursor()) as cur:
            data = (cur.execute("SELECT * FROM users WHERE id =?", (username.lower(),))).fetchall()

            if data:
                raise exceptions.AccountAlreadyExists(f"{username} is already an account")
            else:
                data = (cur.execute("SELECT * from users WHERE email = ?", (email.lower(), ))).fetchall()
                if data:
                    raise exceptions.AccountAlreadyExists(f"An account with {email} already exists")

            cur.execute(
                """INSERT INTO users (email, id, password)
                    VALUES (?, ?, ?)""",
                (email, username.lower(), password),
            )

            return True
