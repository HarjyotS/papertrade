import sys
path = sys.path[0].split("/")
path.pop()
path = "/".join(path)
sys.path.append(path)

from backend import trader


TechBro = trader.Trader(100000, trader.example_user_data)
TechBro.buy("BTC-USD", 1)
print("\n\n\n")
TechBro.sell("BTC-USD", 1)
