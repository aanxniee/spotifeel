# mood profiles with ranges for different audio features

MOOD_PROFILES = {
    'neutral': {
        'valence': (0.3, 0.5),
        'energy': (0.3, 0.5),
        'danceability': (0.3, 0.5),
        'tempo': (90, 110)
    },
    'calm': {
        'valence': (0.0, 0.4),
        'energy': (0.0, 0.4),
        'danceability': (0.0, 0.4),
        'tempo': (60, 90)
    },
    'happy': {
        'valence': (0.5, 1.0),
        'energy': (0.5, 1.0),
        'danceability': (0.5, 1.0),
        'tempo': (100, 200)
    },
    'sad': {
        'valence': (0.0, 0.3),
        'energy': (0.0, 0.4),
        'danceability': (0.0, 0.3),
        'tempo': (60, 90)
    },
    'angry': {
        'valence': (0.2, 0.5),
        'energy': (0.7, 1.0),
        'danceability': (0.4, 0.6),
        'tempo': (120, 180)
    },
    'fearful': {
        'valence': (0.0, 0.4),
        'energy': (0.4, 0.6),
        'danceability': (0.3, 0.5),
        'tempo': (90, 120)
    },
    'disgust': {'valence': (0.0, 0.3),
                'energy': (0.4, 0.6),
                'danceability': (0.2, 0.4),
                'tempo': (90, 110)
                },
    'surprised': {'valence': (0.6, 1.0),
                  'energy': (0.6, 1.0),
                  'danceability': (0.5, 0.8),
                  'tempo': (100, 150)
                  },
}
