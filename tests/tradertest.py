import sys
import os
os.chdir("..")
sys.path.append(os.getcwd())

from backend import trader

#TechBro = trader.Trader.default()
TechBro = trader.Trader.from_file(name="TechBro")
TechBro.buy("BTC-USD", 0.001)
print(TechBro.transaction_history)
TechBro.watch()
