import sys
sys.path.append("")
import utils.fetch_data as fetch
import utils.exceptions as exceptions

example_user_data = {
"BTC-USD": 3,
"DOGE-USD": 1000,
}


class Trader:
    def __init__(self, cash: int, portfolio: dict):
        self.cash = cash
        self.portfolio = portfolio

    def show_balance(self):
        print("Current Balance:", self.cash)
        print("Coins:", self.portfolio)


    def buy(self, coin, quantity):
        current_coin_price = fetch.get_current_price(coin)

        if current_coin_price * quantity > self.cash:
            raise exceptions.BalanceTooLittle("You do not have enough money to make that purchase")

        self.portfolio[coin] += quantity
        self.cash -= (current_coin_price * quantity)

        print(f"Bought {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        self.show_balance()


    def sell(self, coin, quantity):
        if self.portfolio[coin] < quantity:
            raise exceptions.NotEnoughCoins("You do not have enough coins to sell")

        current_coin_price = fetch.get_current_price(coin)

        self.portfolio[coin] -= quantity
        self.cash += (current_coin_price * quantity)

        print(f"Sold {quantity} {coin} for {current_coin_price} USD each")
        print("Total:", current_coin_price * quantity)
        self.show_balance()
