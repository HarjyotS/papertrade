import sys

path_list = sys.path[0].split("\\")
path_list.pop()
path_str = "\\".join(path_list)
sys.path.append(path_str)

from backend import trader

TechBro = trader.Trader.from_file("user_data.json")
TechBro.buy("BTC-USD", 1)
