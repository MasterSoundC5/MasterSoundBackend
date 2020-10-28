import os

from flask import request, jsonify
from flask_restful import Resource
import requests

from app.master_sound.api.schemas import AlbumSchema, ArtistSchema, SongSchema
from app.master_sound.models import Album, Artist, Song
from app.spotify_api import get_token


class AlbumListResource(Resource):
    def get(self):
        if not os.getenv('SPOTIFY_TOKEN'):
            get_token()
        token = os.getenv('SPOTIFY_TOKEN')
        result = []
        header = {'Authorization': f'Bearer {token}'}
        r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header)
        if r.status_code == 401:
            get_token()
            token = os.getenv('SPOTIFY_TOKEN')
            r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header)
        if r.status_code == 200:
            try:
                data = r.json()['albums']['items']
                for item in data:
                    spt_album_id = item['id']
                    cover_image_url = item['images'][0]['url']
                    name = item['name']
                    artists = []
                    for artist in item['artists']:
                        r_artist = requests.get(artist['href'], headers=header)
                        if r_artist.status_code == 200:
                            artist_cover_img_url = r_artist.json()['images'][0]['url']
                            spt_artist_id = artist['id']
                            artist_name = artist['name']
                        else:
                            continue
                        artists.append({
                            'spt_artist_id': spt_artist_id,
                            'name': artist_name,
                            'cover_image_url': artist_cover_img_url
                           })
                    result.append({
                       'spt_album_id': spt_album_id,
                       'cover_image_url': cover_image_url,
                       'name': name,
                       'artists': artists
                       })
                return result, 200
            except Exception as e:
                print(e)
        else:
            return jsonify({'msg': 'Couldn\'t get the albums. Try again.'})

