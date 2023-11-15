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
    <div>
      <h1>Spotifeel</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <input
          type="text"
          value={username}
          onChange={handleUsernameChange}
          placeholder="Username"
        />
        <button type="submit">Upload and Generate Playlist</button>
      </form>
      {playlist && (
        <div>
          <h2>Generated Playlist</h2>
          <p>Mood: {playlist.result}</p>
          <p>
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
