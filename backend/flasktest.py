from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from marshmallow import Schema, fields


class BarQuerySchema(Schema):
    key1 = fields.Str(required=True)
    key2 = fields.Str(required=True)

app = Flask(__name__)
api = Api(app)
schema = BarQuerySchema()


class BarAPI(Resource):
    def get(self):
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))

        return jsonify(request.args)

api.add_resource(BarAPI, '/bar', endpoint='bar')

# omit of you intend to use `flask run` command
if __name__ == '__main__':
    app.run(debug=True)
