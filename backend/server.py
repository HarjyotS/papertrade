import os
import sys
os.chdir("..")
sys.path.append(os.getcwd())
os.chdir(sys.path[0])

import utils.utils as utils
import utils.exceptions as exceptions
import schemas
from trader import Trader
from auth.register import register
from auth.login import login

from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from marshmallow import Schema, fields
import sqlite3
from contextlib import closing

app = Flask(__name__)
api = Api(app)


class Login(Resource):
    def post(self):
        errors = schemas.LoginSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        args = request.args

        try:
            token = login(username=args['username'], password=args['password'])
        except Exception as error:
            abort(400, str(error))

        if token:
            return jsonify({'message': 'success', 'token': token.decode('utf-8')})



class Register(Resource):
    def post(self):
        errors = schemas.RegisterSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        args = request.args

        re = register(email=args['email'], id=args['username'], password=args['password'])
        if re:
            return jsonify({'message': 'success'})
        else:
            abort(400)


class ManageUser(Resource):
    def post(self): #Make sure user is rate limited so they cannot create 1000 accounts
        errors = schemas.CreateUserSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        with closing(sqlite3.connect("user_data.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                new_user = Trader.new_user(**request.args)
                new_user.initial_save_data(cursor)

        return jsonify({'message': f"Succesfully created user {new_user.username} with starting cash of {new_user.cash}"})


    def delete(self): #Make sure user is authorized to delete their own account
        errors = schemas.DeleteUserSchema().validate(request.args)
        if errors:
            abort(400, str(errors))

        with closing(sqlite3.connect("user_data.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                "DELETE from UserData WHERE username = ?",
                (request.args['username'], )
                )

        return jsonify({'message': "Success"})


class TraderAPI(Resource):
    def get(self, username):
        errors = schemas.GetUserDataSchema().validate(request.args)

        with closing(sqlite3.connect("user_data.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    trader = Trader.from_db(cursor, username=username)
                except exceptions.AccountDoesNotExist as error:
                    errors[username] = "Account does not exist."

        if errors:
            abort(400, str(errors))


        if request.args.get('asset'):
            data = getattr(trader, request.args['asset'])
        else:
            data = trader.to_dict()

        return jsonify(data)


class BuySell(Resource):
    operation = None

    def post(self, username):
        errors = schemas.BuySellSchema().validate(request.args)

        with closing(sqlite3.connect("user_data.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    trader = Trader.from_db(cursor, username=username)

                    try:
                        func = getattr(trader, self.operation)
                        res = func(request.args['coin'], float(request.args['quantity']))
                        trader.save_data(cursor)
                    except exceptions.TradeError as error:
                        errors["TradeError"] = error

                except exceptions.AccountDoesNotExist as error:
                    errors[username] = "Account does not exist."

        if errors:
            abort(400, str(errors))

        data = {
        'message': res,
        }

        return jsonify(data)


class Buy(BuySell):
    operation = "buy"

class Sell(BuySell):
    operation = "sell"


api.add_resource(TraderAPI, '/trader/<string:username>')
api.add_resource(Buy, '/trader/<string:username>/buy', endpoint='trader/buy')
api.add_resource(Sell, '/trader/<string:username>/sell', endpoint='trader/sell')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(ManageUser, '/manage')


if __name__ == '__main__':
    app.run(debug = True)
