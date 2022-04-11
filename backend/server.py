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

path = f"{os.getcwd()}/user_data.csv"
def update_data(path=path):
    return utils.csv_to_list(path)

def get_user(name):
    for user in example_data:
        if user['name'] == name:
            return user

app = Flask(__name__)
api = Api(app)
example_data = update_data() #Hook up SQLIte database and convert it into a list of dictionaries


class ManageUser(Resource):
    def post(self): #Make sure user is rate limited so they cannot create 1000 accounts
        errors = schemas.CreateUserSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        new_user = Trader.new_user(**request.args)

        return jsonify({'message': f"Succesfully created user {new_user.name} and id {new_user.id} with starting cash of {new_user.cash}"})


    def delete(self): #Make sure user is authorized to delete their own account
        errors = schemas.DeleteUserSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        res = utils.del_user(path, request.args['name'])

        return jsonify({'message': res})


class TraderAPI(Resource):
    def get(self, name):
        global example_data
        example_data = update_data()

        errors = schemas.GetUserDataSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        user_data = get_user(name)
        if not user_data:
            abort(404, f"User {name} not found")

        trader = Trader.from_dict(user_data)

        if request.args.get('asset'):
            data = getattr(trader, request.args['asset'])
        else:
            data = trader.to_dict()

        return jsonify(data)


class BuySell(Resource):
    operation = None

    def post(self, name):
        errors = schemas.BuySellSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        user_data = get_user(name)
        if not user_data:
            abort(404, f"User {name} not found")

        trader = Trader.from_dict(user_data)

        try:
            func = getattr(trader, self.operation)
            res = func(request.args['coin'], float(request.args['quantity']))
        except exceptions.TradeError as error:
            res = str(error)

        data = {
        'message': res,
        }

        global example_data
        example_data = update_data()

        return jsonify(data)


class Buy(BuySell):
    operation = "buy"

class Sell(BuySell):
    operation = "sell"


api.add_resource(TraderAPI, '/trader/<string:name>')
api.add_resource(Buy, '/trader/<string:name>/buy', endpoint='trader/buy')
api.add_resource(Sell, '/trader/<string:name>/sell', endpoint='trader/sell')

api.add_resource(ManageUser, '/manage')


if __name__ == '__main__':
    app.run(debug = True)
