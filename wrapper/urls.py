from dataclasses import dataclass


@dataclass
class URLs:
    schema = "http://"
    base_url = "localhost:5000"
    register = "/register"
    login = "/login"
    portfolio = "/trader"
    buy = "/buy"
    sell = "/sell"


    @classmethod
    def get_login_url(self, **kwargs):
        return f"{self.schema}{self.base_url}{self.login}", {**kwargs}


    @classmethod
    def get_portfolio_url(self, token):
        return f"{self.schema}{self.base_url}{self.portfolio}", {'token': token}


    @classmethod
    def get_buy_url(self, token, coin, amount):
        return f"{self.schema}{self.base_url}{self.portfolio}{self.buy}?coin={coin}&amount={amount}", {'token': token}


    @classmethod
    def get_sell_url(self, token, coin, amount):
        return f"{self.schema}{self.base_url}{self.portfolio}{self.sell}?coin={coin}&amount={amount}", {'token': token}
