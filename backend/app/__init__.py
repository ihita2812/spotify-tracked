# backend/app/__init__.py

from flask import Flask
from app.routes.route_auth import api_bp as auth_bp

def create_app():
    app = Flask(__name__)

    # load config from .env
    app.config.from_object('app.config.Config')

    # register blueprints
    app.register_blueprint(auth_bp)

    # simple route
    @app.route('/')
    def home():
        return "Welcome to the Spotify Tracked Backend!"

    @app.route('/ping')
    def ping():
        return {"status": "ok", "message": "pong"}

    return app