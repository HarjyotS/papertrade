import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from utils import fetch_data as fetch
import requests

api = "http://localhost:5000"


# Create a new user TechBro with a million dollars
args = {
"email": "john@gmail.com",
"password": "abc123",
"username": "TechBro",
"StartingCash": "1000000"
}

ret = requests.post(f"{api}/register", headers={**args}).json()
print(ret)


# Login to the account you just created
args = {
    "username": "TechBro",
    "password": "abc123"
}

ret = requests.post(f"{api}/login", headers={**args}).json()
token = ret.get('token')
print(ret)

#Token should not be None
assert token != None


# See the TechBro's portfolio
args = {
"token": token
}

data = requests.get(f"{api}/trader", headers={**args}).json()
print(data)

#Should be 1 million dollars in cash and username should be correct
assert data['cash'] == 1000000
assert data['username'] == "techbro"


# Buy 20 BTC
args = {
"token": token
}

ret = requests.post(f"{api}/trader/buy?coin=BTC-USD&amount=20", headers={**args}).json()
print(ret)

data = requests.get(f"{api}/trader", headers={**args}).json()
print(data)
assert data['cash'] == 1000000 - (fetch.get_current_price("BTC-USD") * 20)
assert data['portfolio']['BTC-USD'] == 20


# Sell all BTC
args = {
"token": token
}

ret = requests.post(f"{api}/trader/sell?coin=BTC-USD&amount=20", headers={**args}).json()
print(ret)

data = requests.get(f"{api}/trader", headers={**args}).json()
print(data)
#Should be 0 Bitcoin and original starting amount in cash
assert data['cash'] == 1000000
assert data['portfolio']['BTC-USD'] == 0


# Delete the user
args = {
"token": token
}


ret = requests.delete(f"{api}/manage", headers={**args}).json()
print(ret)
