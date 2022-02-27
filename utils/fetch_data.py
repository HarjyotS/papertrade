from webbrowser import get
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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
