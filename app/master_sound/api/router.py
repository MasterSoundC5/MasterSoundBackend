from flask import request, Blueprint
from flask_restful import Api

from .resources.user_resource import SignUpResource, LoginResource
from .resources.album_resource import AlbumListResource
from .resources.song_resource import SongListResource

master_sound_api = Blueprint('master_sound_api', __name__)

api = Api(master_sound_api)

api.add_resource(SignUpResource, '/api/auth/signup', endpoint='signup_resource')
api.add_resource(AlbumListResource, '/api/albums/new-releases', endpoint='albums_list_resource')
api.add_resource(SongListResource, '/api/albums/<album_id>/songs', endpoint='songs_list_resource')
api.add_resource(LoginResource, '/api/auth/login', endpoint='login_resource')

