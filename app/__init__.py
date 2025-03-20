# Flask app factory
from flask import Flask, make_response
from .routes import healthz,bucketz
from .models import db
from datetime import datetime, timezone
from app.config import Config
from sqlalchemy import create_engine, text

def add_common_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response


def create_database():
    """ Ensure the database exists before creating tables. """
    engine = create_engine(f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}/{Config.DB_NAME}")
    with engine.connect() as connection:
        existing_databases = connection.execute(text("SHOW DATABASES;"))
        # db_names = [row[0] for row in existing_databases]
        #
        # if Config.DB_NAME not in db_names:
        #     connection.execute(text(f"CREATE DATABASE {Config.DB_NAME};"))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config settings from Config class
    db.init_app(app)  # Initialize the database

    # Ensure database exists before creating tables
    create_database()

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    # Register Blueprint
    app.register_blueprint(healthz)
    app.register_blueprint(bucketz)
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error=None):
        response = make_response("", 404)
        return add_common_headers(response)

    @app.errorhandler(405)
    def method_not_allowed(error=None):
        response = make_response("", 405)
        return add_common_headers(response)

    @app.errorhandler(500)
    def internal_server_error(error=None):
        response = make_response("", 500)
        return add_common_headers(response)

    return app


