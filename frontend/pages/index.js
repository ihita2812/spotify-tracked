import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [accessToken, setAccessToken] = useState(null);

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  // Handle login click
  const handleLogin = () => {
    window.location.href = `${backendUrl}/auth/login`;
  };

  // When redirected back from Spotify, parse access_token from URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("access_token");
    if (token) {
      setAccessToken(token);
      fetchTopGenres(token);
      window.history.replaceState({}, "", "/"); // remove query params
    }
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Spotify Wrapped Clone</h1>
      {!accessToken && (
        <button onClick={handleLogin} style={{ padding: "1rem", fontSize: "1rem" }}>
          Login with Spotify
        </button>
      )}
      {accessToken && (
        <div>
          <h2>Top Genres</h2>
          <ul>
            {topGenres.map((g, i) => (
              <li key={i}>{g.genre} ({g.count})</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
