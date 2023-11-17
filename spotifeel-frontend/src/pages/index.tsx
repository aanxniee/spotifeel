import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import { getAccessToken } from "../SpotifyAuth";

type PlaylistResponse = {
  result: string;
  uri: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [playlist, setPlaylist] = useState<PlaylistResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const token = getAccessToken();
  console.log(token);
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

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
    } finally {
      setIsLoading(false);
    }
  };

  const extractPlaylistId = (uri: string) => {
    const parts = uri.split(":");
    return parts[parts.length - 1];
  };

  return (
    <div className="flex flex-col justify-center items-center gap-5">
      <h1 className="text-4xl text-neutral-100">Spotifeel</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <input
          type="file"
          className="mt-5 file-input text-neutral-100 file-input-bordered w-full max-w-xs"
          onChange={handleFileChange}
        />
        <button className="btn text-neutral-100" type="submit">
          Generate Playlist
        </button>
      </form>

      {isLoading && (
        <span className="text-neutral-100 loading loading-dots loading-lg"></span>
      )}
      {playlist && (
        <div className="mt-5 flex flex-col justify-center items-center gap-3 text-neutral-100 font-poppins">
          <h2 className="text-2xl">Generated Playlist</h2>
          <p className="text-xl">Mood: {playlist.result}</p>
          <p className="text-xl">Playlist: {playlist.uri}</p>
        </div>
      )}
    </div>
  );
}
