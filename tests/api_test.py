import requests

# Create a new user TechBro with a million dollars
print(requests.post("http://localhost:5000/manage?name=TechBro&starting_cash=1000000").json())
# See the TechBro's portfolio
print(requests.get("http://localhost:5000/trader/TechBro").json()
)
# Buy 20 BTC
print(requests.post("http://localhost:5000/trader/TechBro/buy?coin=BTC-USD&quantity=20").json()
)
# See the TechBro's portfolio
print(requests.get("http://localhost:5000/trader/TechBro").json()
)
# Sell all BTC
print(requests.post("http://localhost:5000/trader/TechBro/sell?coin=BTC-USD&quantity=20").json()
)
# See the TechBro's portfolio
print(requests.get("http://localhost:5000/trader/TechBro").json()
)
# Delete the user
print(requests.delete("http://localhost:5000/manage?name=TechBro").json()
)
