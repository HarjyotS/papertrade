import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")


def get_current_price(currency):
    data = yf.download(tickers=currency, period="1d", interval="1m")
    return data.iloc[-1]["Close"]


def get_historic_price(currency, time):
    currency = yf.Ticker(currency)
    data = currency.history(period="max").reset_index()
    return data.loc[data["Date"] == time]["Close"]


def get_period_price(currency, period):
    return yf.download(tickers=currency, period=period, interval="1m")
