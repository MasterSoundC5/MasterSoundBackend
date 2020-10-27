import sys

from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash

from ..schemas import UserSchema, CountrySchema
from ...models import User, Country

user_schema = UserSchema()

class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        data['password'] = generate_password_hash(data['password']).decode('utf8')
        user_dict = user_schema.load(data)
        user = User(**user_dict)
        country = Country.get_by_id(user_dict['country_id'])
        user.country = country
        try:
            user.save()
        except Exception as e:
            print(e)
        try:
            print(user)
            response = user_schema.dump(user)
        except Exception as e:
            print(e)
        return response, 201

