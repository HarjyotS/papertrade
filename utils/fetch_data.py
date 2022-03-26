import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import exceptions

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

sns.set_theme(style="darkgrid")


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
        return yf.download(tickers=currency, period=period, interval="1m")
