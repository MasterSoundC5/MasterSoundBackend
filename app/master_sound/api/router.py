from flask import request, Blueprint
from flask_restful import Api

from .resources.user_resource import SignUpResource

master_sound_api = Blueprint('master_sound_api', __name__)

api = Api(master_sound_api)

api.add_resource(SignUpResource, '/api/auth/signup', endpoint='signup_resource')

