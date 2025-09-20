# backend/app/auth/oauth.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

router = APIRouter(prefix="/auth", tags=["auth"])

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played",
        cache_path=".spotify_cache"
    )

@router.get("/login")
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(request: Request):
    sp_oauth = get_spotify_oauth()
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code returned from Spotify"}

    token_info = sp_oauth.get_access_token(code, as_dict=True)
    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"]

    # For now, return token info in JSON (later store in DB)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": token_info["expires_in"]
    }
