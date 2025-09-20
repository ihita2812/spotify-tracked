"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [status, setStatus] = useState<"idle" | "cool" | "not cool">("idle");

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

  // Redirect user to Spotify login
  const handleLogin = () => {
    window.location.href = `${backendUrl}/auth/login`;
  };

  useEffect(() => {
    // Parse query params from redirect
    const params = new URLSearchParams(window.location.search);
    const success = params.get("success");

    if (success === "true") setStatus("cool");
    else if (success === "false") setStatus("not cool");

    // Clean up URL
    window.history.replaceState({}, "", "/");
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Spotify Tracked - Frontend</h1>

      {status === "idle" && (
        <button
          onClick={handleLogin}
          style={{ padding: "1rem", fontSize: "1rem" }}
        >
          Login with Spotify
        </button>
      )}

      {status === "cool" && <h2>cool</h2>}
      {status === "not cool" && <h2>not cool</h2>}
    </div>
  );
}
