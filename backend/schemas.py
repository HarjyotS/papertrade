from marshmallow import Schema, fields, validates, ValidationError
import utils.utils as utils
import os

class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    starting_cash = fields.Float(required=True)

class DeleteUserSchema(Schema):
    name = fields.Str(required=True)

    @validates("name")
    def validate_name(self, name):
        users = utils.csv_to_list(f"{os.getcwd()}/user_data.csv")
        for user_data in users:
            if user_data['name'] == name:
                return
        else:
            raise ValidationError(f"User {name} not found")


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
