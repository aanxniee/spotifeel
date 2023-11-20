import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import { getAccessToken } from "../SpotifyAuth";
import { useAudioRecorder, RecordingState } from "../AudioRecorder";

type PlaylistResponse = {
  result: string;
  uri: string;
};

interface MoodMessages {
  [key: string]: string;
}

const MOOD_MESSAGES: MoodMessages = {
  neutral: "here's something to keep you balanced.",
  calm: "relax and unwind with these tunes.",
  happy: "let's keep the good vibes going!",
  sad: "it might be rough right now, but cheer up!",
  angry: "some tracks to help you cool down.",
  fearful: "music to comfort you in times of fear.",
  disgust: "shake off the bad vibes with these.",
  surprised: "surprise! hope these tracks amaze you.",
};

const getMessageForMood = (mood: string): string => {
  return MOOD_MESSAGES[mood] || "enjoy these tunes!";
};

const createEmbedUrl = (uri: string) => {
  const playlistIdMatch = uri.match(/playlist\/([a-zA-Z0-9]+)/);
  if (playlistIdMatch && playlistIdMatch[1]) {
    const playlistId = playlistIdMatch[1];
    return `https://open.spotify.com/embed/playlist/${playlistId}?utm_source=generator`;
  } else {
    console.error("Invalid Spotify URL");
    return null;
  }
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [playlist, setPlaylist] = useState<PlaylistResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [userChoice, setUserChoice] = useState<"upload" | "record" | null>(
    null
  );
  const { startRecording, stopRecording, recordingState, audioURL } =
    useAudioRecorder();

  const token = getAccessToken();
  console.log(token);

  const handleUserChoice = (choice: "upload" | "record") => {
    setUserChoice(choice);
    setFile(null);
    setErrorMessage(null);
    setPlaylist(null);
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setErrorMessage(null);
    setPlaylist(null);

    if (!file || !token) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<PlaylistResponse>(
        "http://localhost:5000/api/audio",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setPlaylist(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
      setErrorMessage(
        ". . . audio file could not be read. please ensure the file is in PCM WAV format and is not corrupted . . ."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneratePlaylist = async () => {
    if (!audioURL) {
      console.error("No recorded audio to send");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);
    setPlaylist(null);

    try {
      const audioBlob = await fetch(audioURL).then((r) => r.blob());
      const formData = new FormData();
      formData.append(
        "file",
        new File([audioBlob], "recording.webm", { type: "audio/webm" })
      );

      const response = await axios.post<PlaylistResponse>(
        "http://localhost:5000/api/audio",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setPlaylist(response.data);
    } catch (error) {
      console.error("Error uploading recorded audio:", error);
      setErrorMessage("An error occurred while generating the playlist.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-4xl text-neutral-100">Spotifeel</h1>

      {!userChoice && (
        <div className="choice-buttons flex flex-row gap-5">
          <button
            className="btn text-neutral-100"
            onClick={() => handleUserChoice("upload")}
          >
            Upload Audio File
          </button>
          <button
            className="btn text-neutral-100"
            onClick={() => handleUserChoice("record")}
          >
            Record Audio
          </button>
        </div>
      )}

      {userChoice === "upload" && (
        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <input
            type="file"
            accept=".wav"
            className="mt-5 file-input text-neutral-100 file-input-bordered w-full max-w-xs"
            onChange={handleFileChange}
          />
          <button className="btn text-neutral-100" type="submit">
            Generate Playlist
          </button>
        </form>
      )}

      {userChoice === "record" && (
        <div className="flex flex-col gap-5">
          <div className="flex flex-row gap-5">
            <button
              className="btn text-neutral-100"
              onClick={startRecording}
              disabled={recordingState === "recording"}
            >
              Start Recording
            </button>
            <button
              className="btn text-neutral-100"
              onClick={stopRecording}
              disabled={recordingState !== "recording"}
            >
              Stop Recording
            </button>
          </div>
          {audioURL && recordingState === "recorded" && (
            <>
              <audio src={audioURL} controls />
              <button
                className="btn text-neutral-100"
                onClick={handleGeneratePlaylist}
              >
                Generate Playlist
              </button>
            </>
          )}
        </div>
      )}

      {isLoading && (
        <span className="text-neutral-100 loading loading-dots loading-lg"></span>
      )}
      {errorMessage && (
        <div className="text-lg font-poppins text-neutral-100 italic mt-2">
          {errorMessage}
        </div>
      )}
      {!isLoading && !errorMessage && playlist && (
        <div className="mt-5 flex flex-col justify-center items-center gap-2 text-neutral-100 font-poppins">
          <h2 className="text-xl italic">
            . . . here is the playlist we curated for you . . .
          </h2>
          <p className="text-xl">{getMessageForMood(playlist.result)}</p>
          <iframe
            src={
              playlist && playlist.uri
                ? createEmbedUrl(playlist.uri) || undefined
                : undefined
            }
            width="100%"
            height="400"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy"
            className="rounded-xl my-8"
          ></iframe>
        </div>
      )}
    </div>
  );
}
