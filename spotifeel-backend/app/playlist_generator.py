from dotenv import load_dotenv
import os
import random
import sys
import spotipy
from spotipy import util
from utils.mood_profiles import MOOD_PROFILES

import concurrent.futures

load_dotenv()


def authenticate_token(token):
    try:
        sp = spotipy.Spotify(auth=token)
        print('-----Connected to Spotify-----')
        return sp
    except Exception as e:
        print(f'-----Error Connecting to Spotify: {e}-----')
        return None


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


def select_tracks(sp, mood, top_tracks_uri, max_tracks=500):
    print('-----Selecting tracks-----')
    selected_tracks = []
    random.shuffle(top_tracks_uri)

    for i in range(0, min(len(top_tracks_uri), max_tracks), 50):
        batch = top_tracks_uri[i:i+50]
        try:
            tracks_features = sp.audio_features(batch)
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            continue

        for track_data in tracks_features:
            if track_data:
                score = sum(1 for feature in MOOD_PROFILES[mood] if MOOD_PROFILES[mood]
                            [feature][0] <= track_data[feature] <= MOOD_PROFILES[mood][feature][1])
                if score >= len(MOOD_PROFILES[mood]) / 2:
                    selected_tracks.append(track_data['uri'])

    return selected_tracks


def create_playlist(sp, mood):

    top_artists = analyze_top_artists(sp)
    top_tracks = analyze_top_tracks(sp, top_artists)
    selected_tracks = select_tracks(sp, mood, top_tracks)

    if not selected_tracks:
        print("No tracks selected for the playlist.")
        return None

    print('-----Creating Playlist-----')
    user_id = sp.current_user()['id']
    playlist_name = mood + ' playlist'

    try:
        playlist_data = sp.user_playlist_create(user_id, playlist_name)
        sp.user_playlist_add_tracks(
            user_id, playlist_data['id'], selected_tracks[0:30])
        return playlist_data['external_urls']['spotify']
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return None
