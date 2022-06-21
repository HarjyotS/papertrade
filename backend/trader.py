import sys
import os
import json
import time
import random
from datetime import datetime

from utils import utils, exceptions
import utils.fetch_data as fetch


class Trader:
    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.displayname = kwargs.get('displayname', self.username)
        self.cash = kwargs["cash"]
        self.portfolio = kwargs["portfolio"]
        self.transaction_history = kwargs["transaction_history"]
        self.debug = kwargs.get('debug', False)


    @classmethod
    def new_user(cls, *, username, starting_cash: int):
        user_data = {
        "username": username,
        "displayname": username,
        "cash": float(starting_cash),
        "portfolio": {},
        "transaction_history": []
        }
        trader = cls(**user_data)
        return trader


    def to_dict(self):
        user_data = {
            "username": self.username,
            "displayname": self.displayname,
            "cash": self.cash,
            "equity": self.equity,
            "portfolio": self.portfolio,
            "transaction_history": self.transaction_history,
        }
        return user_data


    #Creates a Trader instance from a dictionary where 'portfolio' and 'transaction_history' are string serialized dictionaries
    @classmethod
    def from_dict(cls, user_data: dict):
        user_data['username'] = str(user_data['username'])
        user_data['displayname'] = str(user_data['displayname'])
        user_data['cash'] = float(user_data['cash'])
        user_data['portfolio'] = json.loads(utils.double_quote_dict(user_data['portfolio']))
        user_data['transaction_history'] = json.loads(utils.double_quote_dict(user_data['transaction_history']))
        return cls(**user_data)


    #Creates a Trader instance from an sqlite database given the username
    @classmethod
    def from_db(cls, cursor, *, username):
        #Returns a dictionary user_data from an sqlite database
        username = username.lower()

        rows = cursor.execute(
        "SELECT username, displayname, cash, portfolio, transaction_history FROM UserData WHERE username = ?",
        (username,),
        ).fetchall()

        print(rows)
        if not rows:
            raise exceptions.AccountDoesNotExist(f"'{username}' is not a valid account")

        data = rows[0]

        user_data = {
        "username": data[0],
        "displayname": data[1],
        "cash": data[2],
        "portfolio": data[3],
        "transaction_history": data[4]
        }

        return cls.from_dict(user_data)


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


    def initial_save_data(self, cursor):
        cursor.execute(
        "INSERT INTO UserData VALUES (?, ?, ?, ?, ?)",
        (self.username, self.displayname, int(self.cash), str(self.portfolio), str(self.transaction_history))
        )

    def save_data(self, cursor):
        cursor.execute(
        "UPDATE UserData SET username = ?, displayname = ?, cash = ?, portfolio = ?, transaction_history = ? WHERE username = ?",
        (self.username, self.displayname, self.cash, str(self.portfolio), str(self.transaction_history), self.username)
        )

    @property
    def equity(self):
        _equity = self.cash
        for ticker in self.portfolio:
            quantity = self.portfolio[ticker]
            _equity += (quantity * fetch.get_current_price(ticker))
        return _equity


    def show_balance(self):
        message = f"""
{datetime.now()}
Current Equity: {self.equity}
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
