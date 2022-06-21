import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from utils import utils, exceptions

import sqlite3
from contextlib import closing


path = utils.get_path_to_database(Path(__file__).parents[1], ['maindb', 'tokens.db'])


def authenticate(token):
    with closing(sqlite3.connect(path, isolation_level=None)) as con:
        with closing(con.cursor()) as cur:
            username = cur.execute(
                "SELECT id FROM tokens WHERE token =?", (token,)
            ).fetchone()
            if not username:
                raise exceptions.InvalidToken("Improper token passed")
            else:
                return username[0]
