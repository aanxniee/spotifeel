// pages/_app.tsx

import React, { useEffect, useState } from "react";
import { AppProps } from "next/app";
import { getAccessToken, handleLogout } from "../SpotifyAuth";
import LoginButton from "../components/LoginButton";
import "../globals.css";

const MyApp = ({ Component, pageProps }: AppProps) => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const token = getAccessToken();
    setToken(token);
  }, []);

  const onLogout = () => {
    setToken(null);
  };

  return (
    <div>
      {!token ? (
        <div className="w-screen h-screen flex flex-col justify-center items-center bg-green-500 gap-5">
          <h1 className="text-4xl text-neutral-100">Spotifeel</h1>
          <p className="text-neutral-100 italic">
            . . . . . dynamic playlist generation based on audio emotion
            recognition . . . . .
          </p>
          <LoginButton />
        </div>
      ) : (
        <div className="w-screen h-screen p-10 flex flex-col items-center justify-center bg-green-500 relative">
          <button
            className="absolute top-10 right-10 btn text-neutral-100"
            onClick={() => handleLogout(onLogout)}
          >
            Logout
          </button>
          <Component {...pageProps} />
        </div>
      )}
    </div>
  );
};

export default MyApp;
