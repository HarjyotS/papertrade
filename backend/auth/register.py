import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from utils import utils, exceptions

import sqlite3
from contextlib import closing


path = utils.get_path_to_database(Path(__file__).parents[1], ['maindb', 'data.db'])


def register(*, email, username, password):
    with closing(sqlite3.connect(path, isolation_level=None)) as con:
        with closing(con.cursor()) as cur:
            data = (
                cur.execute("SELECT * FROM users WHERE id =?", (username.lower(),))
            ).fetchall()

            if data:
                raise exceptions.AccountAlreadyExists(
                    f"{username} is already an account"
                )
            else:
                data = (
                    cur.execute("SELECT * from users WHERE email = ?", (email.lower(),))
                ).fetchall()
                if data:
                    raise exceptions.AccountAlreadyExists(
                        f"An account with {email} already exists"
                    )

            cur.execute(
                """INSERT INTO users (email, id, password)
                    VALUES (?, ?, ?)""",
                (email, username.lower(), password),
            )

            return True
