from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    starting_cash = fields.Int(required=True)

class GetUserDataSchema(Schema):
    name = fields.Str(required=True)

class BuySellSchema(Schema):
    name = fields.Str(required=True)
    operation = fields.Str(required=True)
    coin = fields.Int(required=True)
    amount = fields.Int(required=True)
