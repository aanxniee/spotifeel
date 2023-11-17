export const CLIENT_ID = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID;
export const REDIRECT_URI = process.env.NEXT_PUBLIC_SPOTIFY_REDIRECT_URI;
export const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize";
export const RESPONSE_TYPE = "token";

const SCOPES = [
  "user-library-read",
  "user-top-read",
  "playlist-modify-public",
  "user-follow-read",
];

const SCOPES_URL_PARAM = SCOPES.join(" ");

export const authUrl = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${encodeURIComponent(
  SCOPES_URL_PARAM
)}&response_type=${RESPONSE_TYPE}`;

export const getAccessToken = (): string | null => {
  if (typeof window !== "undefined") {
    const hash = window.location.hash;
    let token = window.localStorage.getItem("spotify_access_token");

    if (!token && hash) {
      token =
        hash
          .substring(1)
          .split("&")
          .find((elem) => elem.startsWith("access_token"))
          ?.split("=")[1] || null;
      window.location.hash = "";
      if (token) {
        window.localStorage.setItem("spotify_access_token", token);
      }
    }

    return token;
  }
  return null;
};

export const handleLogout = (onLogout: () => void): void => {
  window.localStorage.removeItem("spotify_access_token");
  onLogout();
};
