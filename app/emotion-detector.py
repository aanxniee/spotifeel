from random import sample
import librosa as lb
import numpy as np
import soundfile as sf
import os
import glob
import pickle

emotion_mappings = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}


def extract_audio_features(file):
    with sf.SoundFile(file) as sound_file:
        X = sound_file.read(dtype="float32")
        print(X)


def load_audio_data():

    for file in glob.glob("./data/Actor_*/*.wav"):
        print(file)


def main():
    load_audio_data()


if __name__ == '__main__':
    main()
