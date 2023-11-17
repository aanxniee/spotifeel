import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

type PlaylistResponse = {
  result: string;
  uri: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [username, setUsername] = useState<string>("");
  const [playlist, setPlaylist] = useState<PlaylistResponse | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", username);
    console.log(file, username);
    try {
      const response = await axios.post<PlaylistResponse>(
        "http://localhost:5000/api/audio",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setPlaylist(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center bg-green-500 gap-5">
      <h1 className="text-4xl text-neutral-100 font-poppins">Spotifeel</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <input
          type="file"
          className="mt-5 file-input file-input-bordered w-full max-w-xs"
          onChange={handleFileChange}
        />
        <input
          type="text"
          placeholder="Username"
          className="input input-bordered w-full max-w-xs"
          onChange={handleUsernameChange}
        />
        <button className="btn" type="submit">
          Generate Playlist
        </button>
      </form>
      {playlist && (
        <div className="mt-5 flex flex-col justify-center items-center gap-3 text-neutral-100 font-poppins">
          <h2 className="text-2xl">Generated Playlist</h2>
          <p className="text-xl">Mood: {playlist.result}</p>
          <p className="text-xl">
            Playlist URL:{" "}
            <a href={playlist.uri} target="_blank" rel="noopener noreferrer">
              {playlist.uri}
            </a>
          </p>
        </div>
      )}
    </div>
  );
}
