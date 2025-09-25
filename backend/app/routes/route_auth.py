# backend/app/routes/route_auth.py

from flask import Blueprint
from flask_restx import Api
from app.auth.oauth import pinger as auth_ns

api_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

api = Api(api_bp,
          title='Spotify Tracked',
          version='1.0',
          description='Spotify Wrapped style backend')

api.add_namespace(auth_ns)
