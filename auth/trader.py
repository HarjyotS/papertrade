import sys
path_list = sys.path[0].split("/")
path_list.pop()
path_str = "/".join(path_list)
sys.path.append(path_str)

import utils.fetch_data as fetch
import utils.exceptions as exceptions
import json
import time
from datetime import datetime


class Trader:
    def __init__(self, user_data: dict):
        self.equity = user_data["equity"]
        self.cash = user_data["cash"]
        self.portfolio = user_data["portfolio"]
        self.transaction_history = user_data["transaction_history"]


    @classmethod
    def default(cls):
        user_data = {
        "equity": 100000,
        "cash": 100000,
        "portfolio": {},
        "transaction_history": {}
        }
        return cls(user_data)


    @classmethod
    def from_file(cls, file_name):
        with open(f"{sys.path[len(sys.path)-1]}/tests/user_data.json") as file:
            user_data = json.load(file)
        return cls(user_data)


    @staticmethod
    def generate_transaction_id():
        id = time.time().strip(".")
        return id

    @staticmethod
    def log_transaction(**kwargs):
        transaction_data = {
        "id": generate_transaction_id()
        }

    def to_dict(self):
        user_data = {
            "equity": self.equity,
            "cash": self.cash,
            "portfolio": self.portfolio,
            "transaction_history": self.transaction_history,
        }
        return user_data

    def save_data(self):
        user_data = self.to_dict()
        with open(
            f"{sys.path[len(sys.path)-1]}/tests/user_data.json", "w+") as file:
            json.dump(user_data, file)

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

        if current_coin_price * quantity > self.cash:
            raise exceptions.BalanceTooLittle(
                "You do not have enough money to make that purchase"
            )

        self.portfolio[coin] += quantity
        self.cash -= current_coin_price * quantity
        self.save_data()


        print(f"Bought {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        print(self.show_balance())

    def sell(self, coin, quantity):
        if self.portfolio[coin] < quantity:
            raise exceptions.NotEnoughCoins("You do not have enough coins to sell")

        current_coin_price = fetch.get_current_price(coin)

        self.portfolio[coin] -= quantity
        self.cash += current_coin_price * quantity
        self.save_data()

        print(f"Sold {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        print(self.show_balance())

    def watch(self):
        while True:
            print(self.show_balance())
            time.sleep(2)
