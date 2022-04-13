from marshmallow import Schema, fields, validates, ValidationError
import utils.utils as utils
import os

class CreateUserSchema(Schema):
    username = fields.Str(required=True)
    starting_cash = fields.Float(required=True)

class DeleteUserSchema(Schema):
    username = fields.Str(required=True)

class GetUserDataSchema(Schema):
    asset = fields.Str()

    @validates("asset")
    def validate_asset(self, asset):
        assets = ['id', 'name', 'cash', 'equity', 'portfolio', 'transaction_history']
        if not asset in assets:
            raise ValidationError("Not a valid asset")

class BuySellSchema(Schema):
    coin = fields.Str(required=True)
    quantity = fields.Float(required=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
