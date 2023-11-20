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

export const getMessageForMood = (mood: string): string => {
  return MOOD_MESSAGES[mood] || "enjoy these tunes!";
};

export const createEmbedUrl = (uri: string) => {
  const playlistIdMatch = uri.match(/playlist\/([a-zA-Z0-9]+)/);
  if (playlistIdMatch && playlistIdMatch[1]) {
    const playlistId = playlistIdMatch[1];
    return `https://open.spotify.com/embed/playlist/${playlistId}?utm_source=generator`;
  } else {
    console.error("Invalid Spotify URL");
    return null;
  }
};
