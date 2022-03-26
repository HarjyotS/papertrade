import sys

path_list = sys.path[0].split("\\")
path_list.pop()
path_str = "\\".join(path_list)
sys.path.append(path_str)

import utils.fetch_data as fetch
import utils.exceptions as exceptions
import json
import time


class Trader:
    def __init__(self, user_data: dict):
        self.equity = user_data["equity"]
        self.portfolio = user_data["portfolio"]
        self.transaction_history = user_data["transaction_history"]

    @classmethod
    def from_file(cls, file_name):
        with open(
            "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\tests\\user_data.json"
        ) as file:
            user_data = json.load(file)
        return cls(user_data)

    @staticmethod
    def generate_transaction_id():
        id = time.time().strip(".")
        return id

    def to_dict(self):
        user_data = {
            "equity": self.equity,
            "portfolio": self.portfolio,
            "transaction_history": self.transaction_history,
        }
        return user_data

    def save_data(self):
        user_data = self.to_dict()
        with open(
            "C:\\Users\\Harjyot\\Desktop\\code\\papertraded\\papertrade\\tests\\user_data.json",
            "w+",
        ) as file:
            json.dump(user_data, file)

    def show_balance(self):
        message = f"""
        Current Balance:, {self.equity}
        Coins: {self.portfolio}
        """
        return message

    def buy(self, coin, quantity):
        current_coin_price = fetch.get_current_price(coin)

        if current_coin_price * quantity > self.equity:
            raise exceptions.BalanceTooLittle(
                "You do not have enough money to make that purchase"
            )

        self.portfolio[coin] += quantity
        self.equity -= current_coin_price * quantity

        print(f"Bought {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        print(self.show_balance())
        self.save_data()

    def sell(self, coin, quantity):
        if self.portfolio[coin] < quantity:
            raise exceptions.NotEnoughCoins("You do not have enough coins to sell")

        current_coin_price = fetch.get_current_price(coin)

        self.portfolio[coin] -= quantity
        self.equity += current_coin_price * quantity

        print(f"Sold {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        print(self.show_balance())
        self.save_data()


with open("user_data.json") as file:
    print(file.read())
