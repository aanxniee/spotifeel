import React from "react";
import { authUrl } from "../SpotifyAuth";

const LoginButton: React.FC = () => {
  const handleLogin = () => {
    window.location.href = authUrl;
  };

  return (
    <button className="btn text-neutral-100" onClick={handleLogin}>
      Login with Spotify
    </button>
  );
};

export default LoginButton;
