import json
import csv

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


def csv_to_list(path): #returns a list of dicts
    list = []
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            list.append(row)
    return list


def del_user(path, name):
    lines = csv_to_list(path)
    for row in lines:
        if row['name'] == name:
            lines.remove(row)

    with open(path, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writeheader()

        writer.writerows(lines)

    return f"Succesfully deleted user {name}"
