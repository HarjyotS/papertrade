import sys
import os
os.chdir("..")
sys.path.append(os.getcwd())

import csv
import utils.utils as utils

user_data = {'equity': 100000, 'cash': 99953.67355859376, 'portfolio': {'BTC-USD': 0.001}, 'transaction_history': {'id': '1648838496', 'time': '2022-04-01 11:41:36.048317', 'cash': 99953.67355859376, 'equity': 100000, 'coin_purchased': 'BTC-USD', 'amount_purchased': 0.001}}
fieldnames = utils.get_keys_of_dict(user_data)


with open("tests/user_data.csv", mode="w+") as csv_file:
    fieldnames = fieldnames
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerow(user_data)
