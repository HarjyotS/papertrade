import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.chdir("..")
    os.chdir("..")
    sys.path.append(os.getcwd())
    os.chdir(sys.path[0])


from utils import exceptions

import sqlite3
from contextlib import closing

path = f"{Path(__file__).parents[1]}/maindb/tokens.db"


def authenticate(username, token):
    with closing(sqlite3.connect(path, isolation_level=None)) as con:
        with closing(con.cursor()) as cur:
            tok = cur.execute(
                "SELECT token FROM tokens WHERE id =?", (username.lower(),)
            ).fetchone()
            if not tok:
                raise exceptions.AccountDoesNotExist(
                    f"Account: '{username}' does not exist or has not been logged in"
                )
            elif token != tok[0]:
                raise exceptions.InvalidToken("Improper token passed")
            else:
                return True