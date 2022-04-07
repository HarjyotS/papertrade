import json
import csv


def float_to_string(flt: float):
    return str(flt).split('.')[0]


def get_keys_of_dict(dict: dict):
    keys = []
    for key in dict:
        keys.append(key)
    return keys


def double_quote_dict(dict: str):
    return str(dict).replace("'", '"')


def csv_to_list(path): #returns a list of dicts
    list = []
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            list.append(row)
    return list
