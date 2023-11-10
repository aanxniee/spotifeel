from dotenv import load_dotenv
import os
import random
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
from utils.mood_profiles import MOOD_PROFILES

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

    # fetch top artists
    def fetch_top_artists(time_range):
        try:
            top_artists_data = sp.current_user_top_artists(
                limit=50, time_range=time_range)['items']
            for artist in top_artists_data:
                top_artists.add((artist['name'], artist['uri']))
        except Exception as e:
            print(f"Error fetching top artists for {time_range}: {e}")

    # use threading to fetch artist data in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_top_artists, [
                     'short_term', 'medium_term', 'long_term'])

    # fetch followed artists
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
    top_tracks = set()

    def fetch_tracks_data(artist_uri):
        try:
            top_tracks_data = sp.artist_top_tracks(artist_uri)['tracks']
            for track in top_tracks_data:
                top_tracks.add((track['name'], track['uri']))
        except Exception as e:
            print(f"Error fetching top tracks for artist {artist_uri}: {e}")

    # use threading to fetch tracks data in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_tracks_data, top_artists_uri)

    top_tracks_name, top_tracks_uri = zip(*top_tracks)
    print(f'Found {len(top_tracks_name)} tracks: {top_tracks_name}')
    return list(top_tracks_uri)


def select_tracks(sp, top_tracks_uri):
    print('-----Selecting tracks-----')
    mood = os.getenv("MOOD")

    tracks_selected = []
    random.shuffle(top_tracks_uri)
    for track in top_tracks_uri[0:100]:
        track_all_data = sp.audio_features(track)
        for track_data in track_all_data:
            try:
                if all(MOOD_PROFILES[mood][feature][0] <= track_data[feature] <= MOOD_PROFILES[mood][feature][1] for feature in MOOD_PROFILES[mood]):
                    tracks_selected.append(track_data['uri'])
            except KeyError:
                pass
    return tracks_selected


if __name__ == '__main__':
    token = create_token('')
    sp = authenticate_token()

    top_artists = analyze_top_artists(sp)
    top_tracks = analyze_top_tracks(sp, top_artists)
    tracks = select_tracks(sp, top_tracks)
    print(tracks)
