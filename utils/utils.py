import utils.exceptions as exceptions

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

def headers_to_dict(headers):
    dict = {}
    for key in headers.keys():
        dict[key.lower()] = headers[key]
    return dict
