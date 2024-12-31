from flask import Flask
from .extensions import db, migrate
from .resources import initialize_api

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register API routes
    initialize_api(app)

    return app
