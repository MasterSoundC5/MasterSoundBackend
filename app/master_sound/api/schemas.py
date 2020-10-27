from marshmallow import fields

from app.ext import ma


class UserSchema(ma.Schema):
    user_id = fields.Integer(dump_only=True)
    given_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    password = fields.String()
    country_id = fields.Integer()
    birth_date = fields.String()
    sex = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    active = fields.Integer()
    country = fields.Nested('CountrySchema')


class CountrySchema(ma.Schema):
    country_id = fields.Integer(dump_only=True)
    iso = fields.String()
    name = fields.String()
    spanish_name = fields.String()

