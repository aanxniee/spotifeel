from dotenv import load_dotenv
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import concurrent.futures

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
    top_artists = set()

    def fetch_artist_data(time_range):
        try:
            top_artists_data = sp.current_user_top_artists(
                limit=50, time_range=time_range)['items']
            for artist in top_artists_data:
                top_artists.add((artist['name'], artist['uri']))
        except Exception as e:
            print(f"Error fetching top artists for {time_range}: {e}")

    # use threading to fetch artist data in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_artist_data, [
                     'short_term', 'medium_term', 'long_term'])

    try:
        followed_artists_data = sp.current_user_followed_artists(limit=50)[
            'artists']['items']
        for artist in followed_artists_data:
            top_artists.add((artist['name'], artist['uri']))
    except Exception as e:
        print(f"Error fetching followed artists: {e}")

    top_artists_name, top_artists_uri = zip(*top_artists)
    print(f'Found {len(top_artists_name)} artists: {top_artists_name}')
    return list(top_artists_uri)


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
