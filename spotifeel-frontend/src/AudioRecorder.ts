import { useState, useEffect, useCallback } from "react";

export type RecordingState = "idle" | "recording" | "recorded";

export const useAudioRecorder = () => {
  const [recordingState, setRecordingState] = useState<RecordingState>("idle");
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(
    null
  );

  const startRecording = useCallback(async () => {
    if (recordingState !== "idle") return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const options = { mimeType: "audio/webm" };
      const newMediaRecorder = new MediaRecorder(stream, options);

      newMediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setAudioURL(URL.createObjectURL(event.data));
        }
      };

      newMediaRecorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
      };

      newMediaRecorder.start();
      setRecordingState("recording");
      console.log("recording");
      setMediaRecorder(newMediaRecorder);
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  }, [recordingState]);

  const stopRecording = useCallback(() => {
    if (recordingState === "recording" && mediaRecorder) {
      mediaRecorder.stop();
      setRecordingState("recorded");
      setMediaRecorder(null);
    }
  }, [mediaRecorder, recordingState]);

  // Cleanup
  useEffect(() => {
    return () => {
      mediaRecorder?.stream.getTracks().forEach((track) => track.stop());
    };
  }, [mediaRecorder]);

  return { startRecording, stopRecording, recordingState, audioURL };
};
