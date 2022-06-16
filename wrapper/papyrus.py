import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from urls import URLs
from utils import exceptions

import requests
import time

class Trader:
    def __init__(self, token):
        self.token = token

    @property
    def cash(self):
        status_code, data = self.get_user_data()
        print(data)
        return data['cash']

    @property
    def display_name(self):
        status_code, data = self.get_user_data()
        return data['displayname']

    @property
    def equity(self):
        status_code, data = self.get_user_data()
        return data['equity']

    @property
    def portfolio(self):
        status_code, data = self.get_user_data()
        return data['portfolio']

    @property
    def transaction_history(self):
        status_code, data = self.get_user_data()
        return data['transaction_history']


    @classmethod
    def from_token(cls, token):
        self = cls(token=token)
        status_code, data = self.get_user_data()
        if status_code != 200:
            raise exceptions.AuthenticationError(data['message'])
        return cls(token)


    @classmethod
    def from_login(cls, **kwargs):
        url, headers = URLs.get_login_url(**kwargs)
        res = requests.post(url, headers=headers)
        data = res.json()
        if res.status_code == 401:
            raise exceptions.InvalidPassword(data['message'])
        elif res.status_code == 404:
            raise exceptions.AccountDoesNotExist(data['message'])
        elif res.status_code == 200:
            token = data.get('token')
            return cls(token)
        else:
            print("Unsupported status code", res.status_code)


    def get_user_data(self):
        url, headers = URLs.get_portfolio_url(self.token)
        res = requests.get(url, headers=headers)
        data = res.json()
        if res.status_code != 200:
            raise TypeError(f"Unsupported status code: {res.status_code} Data: {data}")
        return res.status_code, data


    def buy(self, coin, amount):
        url, headers = URLs.get_buy_url(self.token, coin, amount)
        res = requests.post(url, headers=headers)
        data = res.json()
        if res.status_code == 400:
            raise exceptions.CurrencyNotSupported(data['message'])
        if res.status_code == 404:
            raise exceptions.BalanceTooLittle(data['message'])
        elif res.status_code == 200:
            print(data['message'])
        else:
            raise TypeError(f"Unsupported status code: {res.status_code} Data: {data}")

        return res.status_code, data


    def sell(self, coin, amount):
        url, headers = URLs.get_sell_url(self.token, coin, amount)
        res = requests.post(url, headers=headers)
        data = res.json()
        if res.status_code == 400:
            raise exceptions.CurrencyNotSupported(data['message'])
        if res.status_code == 404:
            raise exceptions.BalanceTooLittle(data['message'])
        elif res.status_code == 200:
            print(data['message'])
        else:
            raise TypeError(f"Unsupported status code: {res.status_code} Data: {data}")

        return res.status_code, data
