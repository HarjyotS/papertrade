import sys
import pandas as pd
import os
os.chdir("..")
sys.path.append(os.getcwd())

from utils import fetch_data as fetch

ticker = "BTC-USD"
c = fetch.get_period_price(ticker, "1d")


print(c)
print(sys.getsizeof(c))
# save the json to a file
