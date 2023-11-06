from random import sample
import librosa as lb
import numpy as np
import soundfile as sf
import os
import glob
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

EMOTION_MAPPINGS = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

EXPECTED_FEATURE_LENGTH = 180


def extract_audio_features(file, chroma, mfcc, mel):
    with sf.SoundFile(file) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        result = np.array([])

        # 12 chromas of musical octives
        if chroma:
            stft = np.abs(lb.stft(X))
            chroma_features = np.mean(lb.feature.chroma_stft(
                S=stft, sr=sample_rate).T, axis=0).flatten()
            result = np.hstack((result, chroma_features))

        # frequency and time characteristics
        if mfcc:
            mfcc_features = np.mean(lb.feature.mfcc(
                y=X, sr=sample_rate, n_mfcc=40).T, axis=0).flatten()
            result = np.hstack((result, mfcc_features))

        # spectrogram of the frequencies in mel scale (scale of pitches)
        if mel:
            mel_features = np.mean(lb.feature.melspectrogram(
                y=X, sr=sample_rate).T, axis=0).flatten()
            result = np.hstack((result, mel_features))

    return result


def load_audio_data(test_size=0.25):
    x, y = [], []
    for file in glob.glob("../data/Actor_*/*.wav"):
        file_name = os.path.basename(file)
        emotion = EMOTION_MAPPINGS[file_name.split("-")[2]]

        feature = extract_audio_features(
            file, chroma=True, mfcc=True, mel=True)

        if len(feature) != EXPECTED_FEATURE_LENGTH:
            print(
                f"Error with file {file_name}: Expected {EXPECTED_FEATURE_LENGTH} features, got {len(feature)}")
            continue

        x.append(feature)
        y.append(emotion)

    return train_test_split(np.array(x), y, test_size=test_size, random_state=101)


def main():
    X_train, X_test, y_train, y_test = load_audio_data()
    print(f'Features extracted: {X_train.shape[1]}')

    model = MLPClassifier(alpha=0.02, batch_size=256, epsilon=1e-08,
                          hidden_layer_sizes=(400,), learning_rate='adaptive', max_iter=1000)
    model.fit(X_train, y_train)

    filename = 'model.sav'
    pickle.dump(model, open(filename, 'wb'))

    y_pred = model.predict(X_test)
    print(f'Accuracy: {round(accuracy_score(y_test, y_pred) * 100, 2)}%')
    print(classification_report(y_true=y_test, y_pred=y_pred))


if __name__ == '__main__':
    main()
