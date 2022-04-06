import csv
import pandas as pd

def csv_to_dict(path):
    list = []
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            list.append(row)
    return list
