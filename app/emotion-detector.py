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


def extract_audio_features(file, chroma, mfcc, mel):
    with sf.SoundFile(file) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        result = np.array([])

        # 12 chromas of musical octives
        if chroma:
            stft = np.abs(lb.stft(X))
            chroma = np.mean(lb.feature.chroma_stft(
                S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))

        # frequency and time characteristics
        if mfcc:
            mfccs = np.mean(lb.feature.mfcc(
                y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))

        # spectrogram of the frequencies in mel scale (scale of pitches)
        if mel:
            mel = np.mean(lb.feature.melspectrogram(
                y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))

    return result


def load_audio_data():

    for file in glob.glob("../data/Actor_*/*.wav"):
        extract_audio_features(file, chroma=True, mfcc=True, mel=True)


def main():
    load_audio_data()


if __name__ == '__main__':
    main()
