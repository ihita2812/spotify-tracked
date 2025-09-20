# backend/app/auth/oauth.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

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

    # If Spotify didn't return a code
    if not code:
        # Redirect to frontend with failure
        return RedirectResponse("http://localhost:3000/?success=false")

    try:
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]

        # Optionally store tokens in DB here

        # Redirect to frontend with success
        return RedirectResponse("http://localhost:3000/?success=true")

    except Exception as e:
        # If token exchange fails
        print("Error fetching token:", e)
        return RedirectResponse("http://localhost:3000/?success=false")
