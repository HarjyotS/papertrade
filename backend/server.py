from email import header
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from utils import utils, exceptions, schemas
from trader import Trader
from auth.register import register
from auth.login import login
from auth.authenticate import authenticate

import os
from flask import Flask, request, abort, jsonify, render_template, make_response
from flask_restful import Resource, Api
from marshmallow import Schema, fields
import sqlite3
from contextlib import closing

app = Flask(__name__, static_folder='../frontend', template_folder='../templates')
api = Api(app)
user_data_path = utils.get_path_to_database(Path(__file__).parent, ['maindb', 'user_data.db'])
user_login_path = utils.get_path_to_database(Path(__file__).parent, ['maindb', 'data.db'])
tokens_path = utils.get_path_to_database(Path(__file__).parent, ['maindb', 'tokens.db'])
class Home(Resource):
    def get(self):
        # return the index.html file formt he frontend folder
        return app.send_static_file('index.html')

class Dashboard(Resource):
    def get(self):
        # return the dashboard.html file formt he templates folder
        resp = make_response(render_template('dashboard.html', title='Dashboard '))
        resp.headers['Content-type'] = 'text/html; charset=utf-8'

        return resp

class Login(Resource):
    def post(self):
        headers = utils.headers_to_dict(request.headers)
        print(headers)
        errors = schemas.LoginSchema().validate(headers)
        if errors:
            abort(400, str(errors))

        try:
            token = login(username=headers['username'], password=headers['password'])
        except exceptions.AccountDoesNotExist as error:
            abort(404, str(error))
        except exceptions.InvalidPassword as error:
            abort(401, str(error))

        if token:
            return jsonify({'token': token})


class Register(Resource):
    def post(self):
        headers = utils.headers_to_dict(request.headers)
        errors = schemas.RegisterSchema().validate(headers)
        if errors:
            print(errors)
            abort(400, str(errors))

        try:
            register(email=headers['email'], username=headers['username'], password=headers['password'])
        except exceptions.AccountAlreadyExists as error:
            abort(409, str(error))

        with closing(sqlite3.connect(user_data_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                new_user = Trader.new_user(username=(headers['username']).lower(), starting_cash=headers['startingcash'])
                new_user.initial_save_data(cursor)

        return jsonify({'message': f"Successfully created user {new_user.username} with starting cash of {new_user.cash}"})


class ManageUser(Resource):
    def delete(self):
        headers = utils.headers_to_dict(request.headers)
        errors = schemas.AuthSchema().validate(headers)
        if errors:
            abort(400, str(errors))

        try:
            username = authenticate(headers['token'])
        except exceptions.AuthenticationError as error:
            abort(401, str(error))


        with closing(sqlite3.connect(user_data_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                "DELETE from UserData WHERE username = ?",
                (username, )
                )

        with closing(sqlite3.connect(user_login_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                "DELETE from users WHERE id = ?",
                (username, )
                )

        with closing(sqlite3.connect(tokens_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                "DELETE from tokens WHERE id = ?",
                (username, )
                )

        return jsonify({'message': f"Successfully deleted user {username}"})


class TraderAPI(Resource):
    def get(self):
        #Validate arguments
        errors = schemas.GetUserDataSchema().validate(request.args)

        if not errors:
            headers = utils.headers_to_dict(request.headers)
            errors = schemas.AuthSchema().validate(headers)

        if errors:
            abort(400, str(errors))

        #Validate token
        try:
            username = authenticate(headers['token'])
        except exceptions.AuthenticationError as error:
            abort(401, str(error))

        utils.printall(user_data_path, "UserData")
        with closing(sqlite3.connect(user_data_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    trader = Trader.from_db(cursor, username=username)
                except exceptions.AccountDoesNotExist as error:
                    abort(404, str(error))

        if request.args.get('asset'):
            data = getattr(trader, request.args['asset'])
        else:
            data = trader.to_dict()

        return jsonify(data)


class BuySell(Resource):
    operation = None

    def post(self):
        #Check if correct arguments are passed
        errors = schemas.BuySellSchema().validate(request.args)

        if not errors:
            headers = utils.headers_to_dict(request.headers)
            errors = schemas.AuthSchema().validate(headers)

        if errors:
            abort(400, str(errors))

        #Validate token
        try:
            username = authenticate(headers['token'])
        except exceptions.AuthenticationError as error:
            abort(401, str(error))


        with closing(sqlite3.connect(user_data_path, isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    trader = Trader.from_db(cursor, username=username)
                except exceptions.AccountDoesNotExist as error:
                    abort(404, str(error))

                try:
                    func = getattr(trader, self.operation)
                    res = func(request.args['coin'], float(request.args['amount']))
                    trader.save_data(cursor)
                except exceptions.CurrencyNotSupported as error:
                    abort(400, str(error))
                except exceptions.BalanceTooLittle as error:
                    abort(404, str(error))
                except exceptions.NotEnoughCoins as error:
                    abort(404, str(error))

        data = {
        'message': res,
        }

        return jsonify(data)


class Buy(BuySell):
    operation = "buy"

class Sell(BuySell):
    operation = "sell"


api.add_resource(TraderAPI, '/trader')
api.add_resource(Buy, '/trader/buy', endpoint='trader/buy')
api.add_resource(Sell, '/trader/sell', endpoint='trader/sell')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(ManageUser, '/manage')
api.add_resource(Home, '/')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    app.run(debug = True)
