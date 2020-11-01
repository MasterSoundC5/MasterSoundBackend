from flask import request, jsonify
from flask_restful import Resource

from app.master_sound.api.schemas import PlaylistSchema
from app.master_sound.models import Playlist
from app.common.error_handling import ObjectNotFound, AppErrorBaseClass

playlist_schema = PlaylistSchema()


class PlaylistListResource(Resource):
    def get(self, user_id):
        playlists = Playlist.simple_filter(user_id=user_id, favourite=0)
        if not playlists:
            raise ObjectNotFound('There was no playlists for this user.')
        result = playlist_schema.dump(playlists, many=True)
        return result, 200

class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.get_by_id(playlist_id)
        if not playlist:
            raise ObjectNotFound('There was no playlist for this id.')

        result = playlist_schema.dump(playlist)
        return result, 200

    def post(self):
        data = request.get_json()
        playlist = Playlist(**data)

        try:
            playlist.save()
        except Exception as e:
            raise AppErrorBaseClass(f'There was an error while saving the playlist. {e}')

        result = playlist_schema.dump(playlist)
        return result, 200

