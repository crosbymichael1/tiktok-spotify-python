import requests
from TikTokApi import TikTokApi
import json
from secrets import spotify_token, spotify_user_id
from exceptions import ResponseException

class TikTokTrending:
    def __init__(self):
        self.all_song_info = {}

    def tiktok(self):
        api = TikTokApi()
        tiktoks = api.discoverMusic()

        for x in tiktoks:
            song_name = x['cardItem']['title']
            artist = x['cardItem']['description']

            self.all_song_info[song_name] = {
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }

    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": "Tiktok Trending Music",
            "description": "Music of Tiktok",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
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
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        print(response_json)
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self):
        """Add all tiktok into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.tiktok()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

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
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 200 or response.status_code != 201:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json

if __name__ == '__main__':
    tk = TikTokTrending()
    tk.add_song_to_playlist()
