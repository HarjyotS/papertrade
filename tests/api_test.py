import sys
from pathlib import Path

from httpx import StatusCode
sys.path.append(str(Path(__file__).parents[1]))

from utils import fetch_data as fetch
import requests

api = "http://localhost:5000"
testAccountUsername = "techbro"
testAccountPassword = "abc123"
testAccountEmail = "tanujsiripurapu@gmail.com"
testAccountStartingCash = 1000000
testCoin = "BTC-USD"


def get_token(**kwargs):
    args = {
        "username": kwargs.get('username', testAccountUsername),
        "password": kwargs.get('password', testAccountPassword)
    }
    
    res = requests.post(f"{api}/login", headers={**args})
    data = res.json()
    return res, data, data.get('token')


def test_create():
    # Create a new user TechBro with a million dollars
    args = {
    "email": testAccountEmail,
    "password": testAccountPassword,
    "username": testAccountUsername,
    "StartingCash": str(testAccountStartingCash)
    }

    res = requests.post(f"{api}/register", headers={**args})
    data = res.json()
    assert res.status_code == 200, data.get('message')


def test_login():
    # Login to the account you just created
    res, data, token = get_token()
    #Token should not be None
    assert token != None, data.get('message')
    assert res.status_code == 200, data.get('message')
    

def test_portfolio():
    # See the TechBro's portfolio
    res, data, token = get_token()
    args = {
    "token": token
    }

    data = requests.get(f"{api}/trader", headers={**args}).json()

    #Should be 1 million dollars in cash and username should be correct
    assert data.get('cash') == testAccountStartingCash, f"Cash balance should be {testAccountStartingCash} but was actually {data.get('cash')}"
    assert data.get('username') == testAccountUsername, f"Username should be {testAccountUsername} but was actually {data.get('username')}"


def test_buy():
    res, data, token = get_token()
    args = {
    "token": token
    }

    res = requests.post(f"{api}/trader/buy?coin={testCoin}&amount=20", headers={**args})
    data = res.json()
    assert res.status_code == 200, data.get('message') 

    data = requests.get(f"{api}/trader", headers={**args}).json()

    assert data.get('cash') == testAccountStartingCash - (fetch.get_current_price(testCoin) * 20), f"Cash balance should be {testAccountStartingCash - (fetch.get_current_price(testCoin) * 20)} but was actually {data.get('cash')}"
    assert data['portfolio'].get(testCoin) == 20, f"Account should contain 20 {testCoin} but actually contained {data['portfolio'].get(testCoin)} {testCoin}"


def test_sell():
    # Sell all BTC
    res, data, token = get_token()
    args = {
    "token": token
    }

    res = requests.post(f"{api}/trader/sell?coin={testCoin}&amount=20", headers={**args})
    data = res.json()
    assert res.status_code == 200, data.get('message')

    data = requests.get(f"{api}/trader", headers={**args}).json()
    
    #Should be 0 Bitcoin and original starting amount in cash
    assert data.get('cash') == testAccountStartingCash, f"Cash balance should be {testAccountStartingCash} but was actually {data.get('cash')}"
    assert data['portfolio'].get(testCoin) == 0, f"Account should contain 0 {testCoin} but actually contained {data['portfolio'].get(testCoin)} {testCoin}"


def test_delete():
    # Delete the user
    res, data, token = get_token()
    args = {
    "token": token
    }


    res = requests.delete(f"{api}/manage", headers={**args})
    data = res.json()
    assert res.status_code == 200, data.get('message') 
