import React, { ChangeEvent, FormEvent } from "react";

interface UploadFormProps {
  onFileChange: (e: ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
}

export const UploadForm: React.FC<UploadFormProps> = ({
  onFileChange,
  onSubmit,
}) => {
  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-5">
      <input
        type="file"
        accept=".wav"
        className="mt-5 file-input text-neutral-100 file-input-bordered w-full max-w-xs"
        onChange={onFileChange}
      />
      <button className="btn text-neutral-100" type="submit">
        Generate Playlist
      </button>
    </form>
  );
};
