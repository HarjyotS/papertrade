import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2]))

from utils import exceptions

import json
import sqlite3
from contextlib import closing


fieldnames = ["id","name","cash","portfolio","transaction_history"]


def float_to_string(flt: float):
    return str(flt).split('.')[0]


def get_keys_of_dict(dict: dict):
    keys = []
    for key in dict:
        keys.append(key)
    return keys


def double_quote_dict(dict: str):
    return str(dict).replace("'", '"')


def printall(path, table):
    with closing(sqlite3.connect(path, isolation_level=None)) as connection:
        with closing(connection.cursor()) as cur:
            cur.execute(
            f"SELECT * FROM {table}")
            for row in cur.fetchall():
                print(row)


#Converts headers from a HTTP request into a dict
def headers_to_dict(headers):
    dict = {}
    for key in headers.keys():
        dict[key.lower()] = headers[key]
    return dict


#parent_path is a string of the closest path you can get too the database
#dirs is a list of folders (ending with a file) on how to get to the database from parent_path
#ex:
#parent_path = /Users/JohnSmith/Code/papertarde
#dirs = ['backend', 'auth', 'database.db']
def get_path_to_database(parent_path, dirs: list):
    if sys.platform in ['linux', 'linux2', 'darwin']:
        # Linux/Mac
        joiner = "/"

    elif sys.platform == "win32":
        # Windows...
        joiner = "\\"

    else:
        raise TypeError("OS not supported")

    return f"{parent_path}{joiner}{joiner.join(dirs)}"
