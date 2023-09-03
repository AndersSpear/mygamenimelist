import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser as cp
import os

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'secrets.cfg')
config = cp.ConfigParser()
config.read(initfile)
SPOTIPY_CLIENT_ID = config.get('SPOTIFY', 'SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = config.get('SPOTIFY', 'SPOTIPY_CLIENT_SECRET')

class Song(object):
    def __init__(self, songdict, detailed=False):
        if detailed:
            self.song_popularity = songdict["popularity"]
            self.song_preview_url = songdict["url"]
            self.song_is_explicit = songdict["is_explicit"]
            self.song_full_artist_list = []
            for artist in songdict["artists"]:
                self.song_full_artist_list.append(artist["name"])
        self.song_name = songdict["name"]
        self.song_primary_artist = songdict["primary_artist"]
        self.album_name = songdict["album"]["name"]
        self.type = "Song"
        self.song_image = songdict["image"]
        self.song_id = songdict["id"]

    def __repr__(self):
        return ("Name: " + self.song_name + "\nArtist: " + self.song_primary_artist + "\nAlbum: " + self.album_name+"\nSong ID: "+self.song_id+"\n")


class SongClient(object):
    def __init__(self):
        creds = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=creds)

    def search(self, search_string):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        result = self.sp.search(search_string, limit=50, offset=0,
                                type='track', market=None)

        songlist = []
        try:
            for track in result["tracks"]["items"]:
                songdict = {}
                songdict["name"] = track["name"]
                songdict["artists"] = track["artists"]
                songdict["primary_artist"] = track["artists"][0]["name"]
                songdict["album"] = track["album"]
                songdict["image"] = track["album"]["images"][0]["url"]
                songdict["id"] = track["id"]
                songdict["popularity"] = track["popularity"]
                songdict["is_explicit"] = track["explicit"]
                songdict["url"] = track["preview_url"]
                song = Song(songdict)
                songlist.append(song)
            return songlist
        except:
            print("Error :(")
            return None

    def get_song(self, song_id):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        result = self.sp.track(song_id)
        songdict = {}
        songdict["name"] = result["name"]
        songdict["artists"] = result["artists"]
        songdict["primary_artist"] = result["artists"][0]["name"]
        songdict["album"] = result["album"]
        songdict["image"] = result["album"]["images"][0]["url"]
        songdict["id"] = result["id"]
        songdict["popularity"] = result["popularity"]
        songdict["is_explicit"] = result["explicit"]
        songdict["url"] = result["preview_url"]
        song = Song(songdict, detailed=True)
        return song


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = SongClient()
    print(client.search("rat")[0])
    print(client.get_song("4blPH3Uy89WnOnYlIv7Ev4"))


# {'disc_number': 1, 'duration_ms': 267066, 'explicit': False, 'external_ids': {'isrc': 'USCM51500238'}, 'external_urls': {'spotify': 'https://open.spotify.com/track/0wwPcA6wtMf6HUMpIRdeP7'}, 'href': 'https://api.spotify.com/v1/tracks/0wwPcA6wtMf6HUMpIRdeP7', 'id': '0wwPcA6wtMf6HUMpIRdeP7', 'is_local': False, 'name': 'Hotline Bling', 'popularity': 80, 'preview_url': 'https://p.scdn.co/mp3-preview/2541ea8f31c87a3bda268b2b7a25bde73530e07d?cid=43c32308e1f940cba0cbcda5c0ecb6d6', 'track_number': 20, 'type': 'track', 'uri': 'spotify:track:0wwPcA6wtMf6HUMpIRdeP7'}
