import requests

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

with open("utils/key.txt") as f:
    API_KEY = f.read()

url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={API_KEY}"
r = requests.get(url)
data = r.json()
print(data)

# Historic data
# https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_{daily/weekly/monthly}&symbol=BTC&market=USD&apikey={API_KEY}

url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=USD&apikey={API_KEY}"
r = requests.get(url)
data = r.json()
print(data)
