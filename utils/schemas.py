import utils.utils as utils

from marshmallow import Schema, fields, validates, ValidationError, EXCLUDE
import os


class GetUserDataSchema(Schema):
    asset = fields.Str()

    @validates("asset")
    def validate_asset(self, asset):
        assets = ['id', 'name', 'cash', 'equity', 'portfolio', 'transaction_history']
        if not asset in assets:
            raise ValidationError("Not a valid asset")


class BuySellSchema(Schema):
    coin = fields.Str(required=True)
    amount = fields.Float(required=True)




class HeaderSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class RegisterSchema(HeaderSchema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    username = fields.Str(required=True)
    displayname = fields.Str()
    startingcash = fields.Float(required=True)


class AuthSchema(HeaderSchema):
    token = fields.Str(required=True)


class LoginSchema(HeaderSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
