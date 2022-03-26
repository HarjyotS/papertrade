import sys
import pandas as pd

path_list = sys.path[0].split("\\")
path_list.pop()
path_str = "\\".join(path_list)
sys.path.append(path_str)

from utils import fetch_data as fetch

ticker = "BTC-USD"
c = fetch.get_period_price(ticker, "1d")


print(c)
print(sys.getsizeof(c))
# save the json to a file
