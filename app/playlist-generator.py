from dotenv import load_dotenv
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost"


def create_token(username):
    scope = "user-library-read user-top-read playlist-modify-public user-follow-read"
    token = util.prompt_for_user_token(
        username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    os.environ['SPOTIFY_TOKEN'] = token
    return token


def authenticate_token():
    if os.getenv("SPOTIFY_TOKEN"):
        token = os.getenv("SPOTIFY_TOKEN")
        print('-----Connected to Spotify-----')
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        print('-----Error Connecting to Spotify-----')
        sys.exit(1)


def analyze_top_artists(sp):
    print('-----Analyzing Top Artists-----')
    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        top_artists_all_data = sp.current_user_top_artists(
            limit=50, time_range=range)
        top_artists_data = top_artists_all_data['items']
        for artist in top_artists_data:
            top_artists_name.append(artist['name'])
            top_artists_uri.append(artist['uri'])

    followed_artists_all_data = sp.current_user_followed_artists(limit=50)
    followed_artists_data = followed_artists_all_data['artists']
    for artist in followed_artists_data['items']:
        if artist['name'] not in top_artists_name:
            top_artists_name.append(artist['name'])
            top_artists_uri.append(artist['uri'])

    print(f'Found {len(top_artists_name)} artists: {top_artists_name}')
    return top_artists_uri


def analyze_top_tracks(sp, top_artists_uri):
    print('-----Analyzing Top Tracks-----')
    top_tracks_name = []
    top_tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all_data = sp.artist_top_tracks(artist)
        top_tracks_data = top_tracks_all_data['tracks']
        for track in top_tracks_data:
            top_tracks_name.append(track['name'])
            top_tracks_uri.append(track['uri'])

    print(f'Found {len(top_tracks_name)} tracks: {top_tracks_name}')
    return top_tracks_uri


if __name__ == '__main__':
    token = create_token('')
    sp = authenticate_token()

    top_artists = analyze_top_artists(sp)
    top_tracks = analyze_top_tracks(sp, top_artists)
