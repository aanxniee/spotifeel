import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import { getAccessToken } from "../SpotifyAuth";
import { useAudioRecorder } from "../AudioRecorder";
import { UploadForm } from "../components/UploadForm";
import { Recorder } from "../components/Recorder";
import { Playlist } from "../components/Playlist";

interface PlaylistResponse {
  result: string;
  uri: string;
}

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
      setErrorMessage("An error occurred while generating the playlist.");
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
        <UploadForm onFileChange={handleFileChange} onSubmit={handleSubmit} />
      )}

      {userChoice === "record" && (
        <Recorder
          onStartRecording={startRecording}
          onStopRecording={stopRecording}
          recordingState={recordingState}
          audioURL={audioURL}
          onGeneratePlaylist={handleGeneratePlaylist}
        />
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
        <Playlist playlist={playlist} />
      )}
    </div>
  );
}
