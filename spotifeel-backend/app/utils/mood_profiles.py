# mood profiles with ranges for different audio features

MOOD_PROFILES = {
    'neutral': {
        'valence': (0.2, 0.6),
        'energy': (0.2, 0.6),
        'danceability': (0.2, 0.6),
        'tempo': (80, 120)
    },
    'calm': {
        'valence': (0.0, 0.5),
        'energy': (0.0, 0.5),
        'danceability': (0.0, 0.5),
        'tempo': (50, 100)
    },
    'happy': {
        'valence': (0.4, 1.0),
        'energy': (0.4, 1.0),
        'danceability': (0.4, 1.0),
        'tempo': (90, 200)
    },
    'sad': {
        'valence': (0.0, 0.4),
        'energy': (0.0, 0.5),
        'danceability': (0.0, 0.4),
        'tempo': (50, 100)
    },
    'angry': {
        'valence': (0.2, 0.6),
        'energy': (0.6, 1.0),
        'danceability': (0.3, 0.7),
        'tempo': (100, 180)
    },
    'fearful': {
        'valence': (0.0, 0.5),
        'energy': (0.3, 0.7),
        'danceability': (0.2, 0.6),
        'tempo': (80, 130)
    },
    'disgust': {
        'valence': (0.0, 0.4),
        'energy': (0.3, 0.7),
        'danceability': (0.1, 0.5),
        'tempo': (80, 120)
    },
    'surprised': {
        'valence': (0.5, 1.0),
        'energy': (0.5, 1.0),
        'danceability': (0.4, 0.9),
        'tempo': (90, 160)
    },
}
