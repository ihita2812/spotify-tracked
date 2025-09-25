# backend/app/auth/oauth.py

from flask import redirect, request
from flask_restx import Namespace, Resource
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config import Config

pinger = Namespace('', description='Authentication related operations')

sp_oauth = SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope="user-follow-read,user-top-read,user-library-read,user-read-recently-played",
            show_dialog=True,
            cache_path=".spotify_cache"
)
        
@pinger.route('/login')
class Login(Resource):
    def get(self):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

@pinger.route('/callback')
class Callback(Resource):
    def get(self):
        code = request.args.get('code')
        if not code:
            return {"error": "you didn't allow a connection i'm sad now"}, 200

        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

        sp = spotipy.Spotify(auth=access_token)

        user_profile = sp.current_user()
        return {"message": "Authentication successful", "user": user_profile}, 200
