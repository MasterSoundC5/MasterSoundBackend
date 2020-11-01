import os

from flask import request, jsonify
from flask_restful import Resource
import requests

from app.master_sound.api.schemas import AlbumSchema, ArtistSchema, SongSchema
from app.master_sound.models import Album, Artist, Song
from app.spotify_api import get_token
from app.common.error_handling import AppErrorBaseClass

album_schema = AlbumSchema(exclude=['songs'])


class AlbumListResource(Resource):
    def get(self):
        albums = Album.get_all()
        print(albums)
        result = album_schema.dump(albums, many=True)
        return result, 200

    def post(self):
        data = request.get_json()
        for _json in data:
            album = Album(cover_image_url=_json['cover_image_url'], spt_album_id=_json['spt_album_id'], album_name=_json['album_name'])
            for artist in _json['artists']:
                new_artist = Artist(spt_artist_id=artist['spt_artist_id'], artist_name=artist['artist_name'], cover_image_url=artist['cover_image_url'])
                album.artists.append(new_artist)
            print(album)
            try:
                album.save()
            except Exception as e:
                print(e)
                raise AppErrorBaseClass(e)
        return {'msg': 'Your albums were saved succesfully.'}, 201

