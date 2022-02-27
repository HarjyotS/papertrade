from webbrowser import get
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt

supported = ["BTC-USD", "ETH-USD", "LTC-USD", "DOGE-USD"]

# yf.download(tickers=argument1, period=argument2, interval=argument3)


def get_data(ticker):
    if ticker in supported:
        return yf.download(ticker, period="22h", interval="1m")


print(get_data("BTC-USD"))
print("\n\n")
print(get_data("ETH-USD"))
print("\n\n")
print(get_data("LTC-USD"))
print("\n\n")
print(get_data("DOGE-USD"))
