from logging import exception
import sqlite3
import time
import os
import base64, hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def login(username, password):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\utils\\maindb\\data.db"
    )
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id =?", (username.lower(),))
        data = cur.fetchone()
        print(data)
        con.commit()
        con.close()
        if data is None:
            return False
        elif data[2] == password:
            iftok = checktok(username)  # check if token exists
            if iftok:
                pass
            else:
                newtok = generatetok()
                insertok(username, newtok)
    except exception as e:
        print(e)
        con.close()
        return False


def insertok(username, key):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\utils\\maindb\\tokens.db"
    )
    cur = con.cursor()
    try:
        cur.execute(
            """INSERT INTO tokens (id, token)
                VALUES (?, ?)""",
            (username.lower(), key),
        )
        con.commit()
        con.close()
        return True
    except exception() as e:
        print(e)
        con.close()
        return False


def generatetok(username):
    # generate random token that has not been used before
    # yes im not checking that it hasnt been usef before because all usernames are unique and i am lazy.
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
    print(key)
    return key


def checktok(username):
    con = sqlite3.connect(
        "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\utils\\maindb\\tokens.db"
    )
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tokens WHERE id =?", (username.lower(),))
        data = cur.fetchone()
        print(data)
        con.commit()
        con.close()
        if data is None:
            return False
        else:
            return True
    except exception() as e:
        print(e)
        con.close()
        return False


generatetok("harjyot")
