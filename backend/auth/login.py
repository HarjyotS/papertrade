import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from utils import utils, exceptions

import os
from atexit import register
from logging import exception
import sqlite3
import time
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from contextlib import closing
from sys import platform


users_path = utils.get_path_to_database(Path(__file__).parents[1], ["maindb", "data.db"])
tokens_path = utils.get_path_to_database(Path(__file__).parents[1], ["maindb", "tokens.db"])


def login(*, username, password):
    with closing(sqlite3.connect(users_path, isolation_level=None)) as connection:
        with closing(connection.cursor()) as cur:
            cur.execute("SELECT * FROM users WHERE id =?", (username.lower(),))
            data = cur.fetchone()
            if data is None:
                raise exceptions.AccountDoesNotExist(f"{username} does not exist")
                return False
            elif data[1] == password:
                iftok = checktok(username)  # check if token exists
                if iftok is not False:
                    return iftok
                else:
                    newtok = generatetok(username)

                    c = insertok(username, newtok)

                    return newtok
            else:
                raise exceptions.InvalidPassword(f"{password} is an invalid password")


def insertok(username, key):
    with closing(sqlite3.connect(tokens_path, isolation_level=None)) as connection:
        with closing(connection.cursor()) as cur:
            cur.execute(
                """INSERT INTO tokens (id, token)
                    VALUES (?, ?)""",
                (username.lower(), key),
            )


def generatetok(username):
    # generate random token that has not been used before
    backend = default_backend()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=backend,
    )
    key = base64.urlsafe_b64encode(kdf.derive((username + str(time.time())).encode()))
    return key.decode("utf-8")


def checktok(username):
    with closing(sqlite3.connect(tokens_path, isolation_level=None)) as con:
        with closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM tokens WHERE id =?", (username.lower(),))
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return data[1]
