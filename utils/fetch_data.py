from utils import exceptions

import json
import sys
import yfinance as yf

supported = [
    "BTC-USD",
    "ETH-USD",
    "USDT-USD",
    "BNB-USD",
    "USDC-USD",
    "XRP-USD",
    "ADA-USD",
    "SOL-USD",
    "LUNA1-USD",
    "HEX-USD",
    "AVAX-USD",
    "BUSD-USD",
    "DOT-USD",
    "DOGE-USD",
    "SHIB-USD",
    "UST-USD",
    "MATIC-USD",
    "CRO-USD",
    "WBTC-USD",
    "DAI-USD",
    "ATOM-USD",
    "LTC-USD",
    "LINK-USD",
    "UNI1-USD",
    "TRX-USD",
    "BCH-USD",
    "FTT-USD",
    "LEO-USD",
    "NEAR-USD",
    "ALGO-USD",
]


def get_current_price(currency):
    if currency in supported:
        ticker = yf.Ticker(currency)
        todays_data = ticker.history(period="1d")
        return todays_data["Close"][0]
    else:
        raise exceptions.CurrencyNotSupported(
            "This currency does not exist or is not supported"
        )


def get_historic_price(currency, time):
    if currency in supported:
        currency = yf.Ticker(currency)
        data = currency.history(period="max").reset_index()
        return data.loc[data["Date"] == time]["Close"]


def get_period_price(currency, period):
    if currency in supported:
        data = yf.download(tickers=currency, period=period, interval="1m")
        data = json.loads(data.to_json(orient="table"))
        newdat = []
        for i in data["data"]:
            if i == 0:
                pass
            else:
                newdat.append({"Date": i["Datetime"], "price": i["Close"]})

        # data = data.to_json(orient="table")

        return newdat
