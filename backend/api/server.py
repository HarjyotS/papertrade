import os
import sys
os.chdir("..")
sys.path.append(os.getcwd())
os.chdir("..")
sys.path.append(os.getcwd())
os.chdir(sys.path[0])

import utils.utils as utils
from flask import Flask, json, jsonify
from flask_restful import Resource, Api, reqparse
from trader import Trader

path = f"{sys.path[len(sys.path)-1]}/backend/api/user_data.csv"
example_data = utils.csv_to_list(path)

def get_user(name):
    for user in example_data:
        if user['name'] == name:
            return user


app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self, name):
        return jsonify(get_user(name))

    def post(self, name, coin, amount):
        trader = Trader.from_dict(get_user(name))
        trader.buy(coin, amount)
        data = {
        'name': name,
        'coin': coin,
        'amount': amount
        }
        return jsonify(data)


api.add_resource(Users, '/users/<string:name>/', '/users/<string:name>/buy/<string:coin>/<int:amount>/')


if __name__ == '__main__':
    app.run(debug = True)
