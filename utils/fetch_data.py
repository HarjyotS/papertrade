import requests


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
