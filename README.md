# 🎵 Spotifeel

Spotifeel is a full-stack dynamic playlist generator based on audio emotion recognition.

## Frontend
The frontend was built on React.js, Next.js, and Typescript. Auth was implemented using Spotify OAuth from Spotify's Web and Web Playback SDK API. Features login/logout connection to your Spotify account, audio upload, and voice recording. Once you upload or record an audio file, the file is sent to the backend via POST request for processing.

# Backend
The backend was built on Python and Flask. The API receives an audio file and uses the SpeechRecognition library to save and read it locally. Audio features are then extracted and fed to the model for prediction. Once it receives the predicted mood from the model, the API selects tracks from the user's top artists to generate a custom playlist, tailored to the user's mood. This playlist is randomized every time so the song recommendations are always different.

# Machine Learning Model

The ML model has the ability to recognize emotions through audio. The model was trained based on the [RAVDESS](https://zenodo.org/records/1188976#.YFZuJ0j7SL8) dataset. The dataset contains audio files that encompass neutral, calm, happy, sad, angry, fearful, surprise, and disgust emotions. For example audio file from the dataset, I extracted and augmented the audio features, such as MFCC, chromal, and mel-spectrogram, using Librosa. The audio features were then processed using scikit-learn and numpy and passed through a MLPClassifer. I also used matplotlib, and seaborn for visualization. The model has an accuracy of 91.77%. This model is an example of supervised learning wherein we have used some data for training and rest of the data for testing the model. I practice supervised learning algorithms, including data augmention, feature engineering, cross-validation, hyperparameter tuning, and regularization.

https://github.com/aanxniee/spotifeel/assets/63011927/d9352e87-3444-4563-981e-f0323d89d403

https://github.com/aanxniee/spotifeel/assets/63011927/b15d9604-bef2-45b8-a450-b4aa219c6305




