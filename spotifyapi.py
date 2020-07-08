import requests
import json
from exceptions import ResponseException
from tiktokv2 import TikTokTrending

class spotify:
    def __init__(self, spotify_user_id, spotify_token):
        self.spotify_user_id = spotify_user_id
        self.spotify_token = spotify_token


    def create_playlist(self,playlist_name, description, public = True):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": playlist_name,
            "description": description,
            "public": public
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        print(response.json())
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        print(response_json)
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self):
        """Add all tiktok songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.tiktok()
        self.all_song_info

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in all_song_info.items()]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 200 or response.status_code != 201:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json
