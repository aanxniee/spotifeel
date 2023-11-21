from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import speech_recognition as sr
import librosa as lb
from werkzeug.utils import secure_filename
import emotion_detector
import playlist_generator
from pydub import AudioSegment

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/audio', methods=['POST'])
def main():

    print("POST request received")
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '')
    else:
        return jsonify({"error": "No token provided"}), 401

    sp = playlist_generator.authenticate_token(token)

    if "file" not in request.files:
        return jsonify({"error": "No file in request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        audio_files_dir = "../audio_files"
        os.makedirs(audio_files_dir, exist_ok=True)

        original_filename = os.path.join(
            audio_files_dir, secure_filename(file.filename))
        file.save(original_filename)

        try:

            file_extension = os.path.splitext(file.filename)[1].lower()

            if file_extension == '.webm':
                webm_audio = AudioSegment.from_file(
                    original_filename, format="webm")
                wav_filename = os.path.splitext(original_filename)[0] + '.wav'
                webm_audio.export(wav_filename, format="wav")
                audio_file = wav_filename
            elif file_extension == '.wav':
                audio_file = original_filename
            else:
                return jsonify({"error": "Unsupported file format"}), 400

            print(audio_file)
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            audio_data, sample_rate = lb.load(audio_file, sr=None)
            audio_features = emotion_detector.extract_audio_features(
                audio_data, sample_rate, mfcc=True, chroma=True, mel=True)

            mood = emotion_detector.predict_mood(audio_features)
            print(mood)

            playlist = playlist_generator.create_playlist(sp, mood)

            return jsonify({"result": mood, "uri": playlist}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
