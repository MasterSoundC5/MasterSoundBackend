import os
from datetime import timedelta

from flask import request, jsonify
from flask_restful import Resource
import requests

from app.spotify_api import get_token


class SongListResource(Resource):
    def get(self, album_id):
        if not os.getenv('SPOTIFY_TOKEN'):
            get_token()
        token = os.getenv('SPOTIFY_TOKEN')
        result = []
        header = {'Authorization': f'Bearer {token}'}
        r = requests.get(f'https://api.spotify.com/v1/albums/{album_id}/tracks', headers=header)
        if r.status_code == 401:
           get_token()
           token = os.getenv('SPOTIFY_TOKEN')
           r = requests.get(f'https://api.spotify.com/v1/albums/{album_id}/tracks', headers=header)
        if r.status_code == 200:
            data = r.json()['items']
            order_number = 1
            for item in data:
                spt_song_id = item['id']
                spt_album_id = album_id
                name = item['name']
                duration = str(timedelta(milliseconds=item['duration_ms']))[2:7]
                sound_url = item['preview_url']
                result.append({
                    'order_number': order_number,
                    'spt_song_id': spt_song_id,
                    'spt_album_id': spt_album_id,
                    'name': name,
                    'duration': duration,
                    'played_song_number': 10,
                    'sound_url': sound_url
                    })
                order_number += 1
            return result, 200
        else:
            return jsonify({'msg': f'There was an error getting the songs. {r.status_code}'})

