import sys
path = sys.path[0].split("/")
path.pop()
path = "/".join(path)
sys.path.append(path)

from utils import fetch_data as fetch

ticker = "BTC-USD"
print(fetch.get_current_price(ticker))
