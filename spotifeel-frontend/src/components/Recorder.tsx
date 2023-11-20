import React from "react";

interface RecorderProps {
  onStartRecording: () => void;
  onStopRecording: () => void;
  recordingState: string;
  audioURL: string | null;
  onGeneratePlaylist: () => void;
}

export const Recorder: React.FC<RecorderProps> = ({
  onStartRecording,
  onStopRecording,
  recordingState,
  audioURL,
  onGeneratePlaylist,
}) => {
  return (
    <div className="flex flex-col mt-5 gap-5">
      <div className="flex flex-row gap-5">
        <button
          className="btn text-neutral-100"
          onClick={onStartRecording}
          disabled={recordingState === "recording"}
        >
          Start Recording
        </button>
        <button
          className="btn text-neutral-100"
          onClick={onStopRecording}
          disabled={recordingState !== "recording"}
        >
          Stop Recording
        </button>
      </div>
      {audioURL && recordingState === "recorded" && (
        <>
          <audio src={audioURL} controls />
          <button className="btn text-neutral-100" onClick={onGeneratePlaylist}>
            Generate Playlist
          </button>
        </>
      )}
    </div>
  );
};
