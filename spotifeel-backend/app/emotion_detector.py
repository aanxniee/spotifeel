import librosa as lb
import numpy as np
import os
import glob
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


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


def extract_audio_features(audio_data, sample_rate, chroma, mfcc, mel):
    result = np.array([])

    # 12 chromas of musical octives
    if chroma:
        stft = np.abs(lb.stft(audio_data))
        chroma_features = np.mean(lb.feature.chroma_stft(
            S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma_features))

    # frequency and time characteristics
    if mfcc:
        mfcc_features = np.mean(lb.feature.mfcc(
            y=audio_data, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfcc_features))

    # spectrogram of the frequencies in mel scale (scale of pitches)
    if mel:
        mel_features = np.mean(lb.feature.melspectrogram(
            y=audio_data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel_features))

    return result


def augment_data(file, n_steps, rate):
    raw = lb.load(file, sr=None)
    pitch_shifted = lb.effects.pitch_shift(raw[0], sr=raw[1], n_steps=n_steps)
    time_stretched = lb.effects.time_stretch(pitch_shifted, rate=rate)
    return time_stretched, raw[1]


def load_and_augment_data(test_size=0.25, n_steps=0.5, rate=1.25):
    x, y = [], []

    for file in glob.glob("../data/Actor_*/*.wav"):
        file_name = os.path.basename(file)

        emotion = EMOTION_MAPPINGS.get(file_name.split("-")[2])
        if emotion is None:
            continue

        audio_data, sample_rate = lb.load(file, sr=None)
        original_features = extract_audio_features(
            audio_data, sample_rate, chroma=True, mfcc=True, mel=True)

        if len(original_features) != EXPECTED_FEATURE_LENGTH:
            continue

        x.append(original_features)
        y.append(emotion)

        augmented_audio, sample_rate = augment_data(
            file, n_steps=n_steps, rate=rate)
        augmented_features = extract_audio_features(
            augmented_audio, sample_rate, chroma=True, mfcc=True, mel=True)

        if len(augmented_features) != EXPECTED_FEATURE_LENGTH:
            continue

        x.append(augmented_features)
        y.append(emotion)

    return train_test_split(np.array(x), y, test_size=test_size, random_state=101)


def main():
    X_train, X_test, y_train, y_test = load_and_augment_data()

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = MLPClassifier(alpha=0.02, batch_size=256, epsilon=1e-08,
                          hidden_layer_sizes=(400, 200, 100), learning_rate='adaptive', max_iter=1000)
    model.fit(X_train_scaled, y_train)

    filename = 'model.sav'
    pickle.dump(model, open(filename, 'wb'))

    y_pred = model.predict(X_test_scaled)

    print(f'Accuracy: {round(accuracy_score(y_test, y_pred) * 100, 2)}%')

    scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    print(f"Cross-validated scores: {scores}")

    print(classification_report(y_true=y_test, y_pred=y_pred))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues',
                xticklabels=EMOTION_MAPPINGS.values(), yticklabels=EMOTION_MAPPINGS.values())
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()


if __name__ == '__main__':
    main()


def predict_mood(audio_features):
    model = pickle.load(open("model.sav", "rb"))
    prediction = model.predict([audio_features])
    return prediction[0]
