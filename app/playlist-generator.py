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
        print('-----Unable to connect to Spotify-----')
        sys.exit(1)


if __name__ == '__main__':
    token = create_token('22incn5g5limprnx32vxycuqq')
    sp = authenticate_token()
