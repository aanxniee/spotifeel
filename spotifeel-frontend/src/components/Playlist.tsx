import React from "react";
import { getMessageForMood, createEmbedUrl } from "../utils";

interface PlaylistResponse {
  result: string;
  uri: string;
}

interface PlaylistProps {
  playlist: PlaylistResponse;
}

export const Playlist: React.FC<PlaylistProps> = ({ playlist }) => {
  return (
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
  );
};
