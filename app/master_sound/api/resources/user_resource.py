from datetime import timedelta

from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

from app.common.error_handling import AppErrorBaseClass
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
            response = user_schema.dump(user)
        except Exception as e:
            print(e)
        return response, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        error = {'msg': 'Email or password invalid'}
        print(data)
        try:
            user = User.simple_filter(email=data['email'])[0]
            print('paso')
        except IndexError as e:
            print(e)
            return error, 200

        authorized = check_password_hash(user.password, data['password'])

        if not authorized:
            return error, 200

        expires = timedelta(days=7)
        access_token = create_access_token(identity=user.user_id, expires_delta=expires)

        return {'access_token': access_token, 'token_type': 'Bearer', 'expires_in': str(expires)}, 200

