import sys
import os
import json
import csv
import time
from datetime import datetime

import utils.utils as utils
import utils.fetch_data as fetch
import utils.exceptions as exceptions


class Trader:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.cash = kwargs["cash"]
        self.portfolio = kwargs["portfolio"]
        self.equity = self.calculate_equity()
        self.transaction_history = kwargs["transaction_history"]
        self.debug = kwargs.get('debug', True)


    @classmethod
    def new_user(cls, *, name, starting_cash: int):
        user_data = {
        "id": cls.generate_id(),
        "name": name,
        "cash": int(starting_cash),
        "portfolio": {},
        "transaction_history": []
        }
        trader = cls(**user_data)
        trader.save_data()
        return trader


    @classmethod
    def default(cls):
        user_data = {
        "id": cls.generate_id(),
        "name": "TechBro",
        "cash": 100000,
        "portfolio": {},
        "transaction_history": []
        }
        return cls(**user_data)


    @classmethod
    def from_dict(cls, user_data: dict):
        user_data['id'] = user_data['id']
        user_data['name'] = str(user_data['name'])
        user_data['cash'] = float(user_data['cash'])
        user_data['portfolio'] = json.loads(utils.double_quote_dict(user_data['portfolio']))
        user_data['transaction_history'] = json.loads(utils.double_quote_dict(user_data['transaction_history']))
        return cls(**user_data)


    @classmethod
    def from_file(cls, path=None, *, name):
        if not path:
            path = f"{sys.path[len(sys.path)-1]}/tests/user_data.csv"

        user_data = utils.csv_to_list(path)
        for row in user_data:
            if row['name'] == name:
                return cls.from_dict(row)


    @staticmethod
    def generate_id():
        id = utils.float_to_string(time.time())
        return id


    @classmethod
    def log_transaction(cls, **kwargs):
        transaction_data = {
        "id": cls.generate_id(),
        "time": str(datetime.now()),
        "cash": kwargs['cash'],
        "equity": kwargs['equity'],
        "coin_purchased": kwargs['coin'],
        "amount_purchased": kwargs['quantity'],
        }
        return transaction_data


    def to_dict(self):
        user_data = {
            "id": self.id,
            "name": self.name,
            "cash": self.cash,
            "equity": self.calculate_equity(),
            "portfolio": self.portfolio,
            "transaction_history": self.transaction_history,
        }
        return user_data


    def save_data(self):
        path = f"{os.getcwd()}/user_data.csv"
        utils.del_user(path, self.name)
        user_data = self.to_dict()
        del user_data['equity']
        fieldnames = utils.get_keys_of_dict(user_data)
        with open(path, mode="a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            #writer.writeheader()

            writer.writerow(user_data)


    def calculate_equity(self):
        equity = self.cash
        for ticker in self.portfolio:
            quantity = self.portfolio[ticker]
            equity += (quantity * fetch.get_current_price(ticker))
        return equity


    def show_balance(self):
        message = f"""
{datetime.now()}
Current Equity: {self.calculate_equity()}
Current Cash Balance: {self.cash}
Coins: {self.portfolio}
        """
        return message


    def buy(self, coin, quantity):
        if not self.portfolio.get(coin):
            self.portfolio[coin] = 0

        current_coin_price = fetch.get_current_price(coin)

        if (current_coin_price * quantity) > self.cash:
            raise exceptions.BalanceTooLittle(
                "You do not have enough money to make that purchase"
            )

        self.portfolio[coin] += quantity
        self.cash -= (current_coin_price * quantity)
        self.transaction_history.append(self.log_transaction(cash=self.cash, equity=self.equity, coin=coin, quantity=quantity))
        self.save_data()


        message = (f"Bought {quantity} {coin} for {current_coin_price} USD each")

        if self.debug:
            print(message)
            print("Total:", current_coin_price * quantity)
            print(self.show_balance())

        return message


    def sell(self, coin, quantity):
        if self.portfolio.get(coin, 0) < quantity:
            raise exceptions.NotEnoughCoins("You do not have enough coins to sell")

        current_coin_price = fetch.get_current_price(coin)

        self.portfolio[coin] -= quantity
        self.cash += current_coin_price * quantity
        self.transaction_history.append(self.log_transaction(cash=self.cash, equity=self.equity, coin=coin, quantity=quantity))
        self.save_data()

        message = (f"Sold {quantity} {coin} for {current_coin_price} USD each")

        if self.debug:
            print(message)
            print("Total:", current_coin_price * quantity)
            print(self.show_balance())

        return message


    def watch(self):
        while True:
            print(self.show_balance())
            time.sleep(2)
