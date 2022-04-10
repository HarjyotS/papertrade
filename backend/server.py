import os
import sys
os.chdir("..")
sys.path.append(os.getcwd())
os.chdir(sys.path[0])

import utils.utils as utils
import utils.exceptions as exceptions
import schemas
from trader import Trader

from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)
example_data = update_data()


def update_data(path=f"{os.getcwd()}/user_data.csv"):
    return utils.csv_to_list(path)

def get_user(name):
    for user in example_data:
        if user['name'] == name:
            return user


class CreateUser(Resource):
    def post(self, name, starting_cash):
        errors = schemas.CreateUserSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        return jsonify(request.args)

        return jsonify({'message': f"Succesfully created user {trader.name} with {trader.cash}"})


class TraderAPI(Resource):
    def get(self, name):
        global example_data
        example_data = update_data()
        return jsonify(get_user(name))

    def post(self, operation, name, coin, amount):
        trader = Trader.from_dict(get_user(name))
        if operation == "buy":
            func = trader.buy
        elif operation == "sell":
            func = trader.sell
        else:
            res = f"Invalid Operation: {operation}"

        if func:
            try:
                res = func(coin, amount)
            except exceptions.TradeError as error:
                res = str(error)

        data = {
        'message': res,
        }

        global example_data
        example_data = update_data()

        return jsonify(data)


api.add_resource(TraderAPI, '/trader/<string:name>/', '/trader/<string:name>/<string:operation>/<string:coin>/<int:amount>/')
api.add_resource(CreateUser, '/createuser/<string:name>/<int:starting_cash>/')

if __name__ == '__main__':
    app.run(debug = True)
