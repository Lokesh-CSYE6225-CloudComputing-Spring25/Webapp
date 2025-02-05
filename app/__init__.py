# Flask app factory
from flask import Flask, make_response
from .routes import healthz
from .models import db
from datetime import datetime
from app.config import Config
from sqlalchemy import create_engine, text

def add_common_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response

def create_database():
    """ Automatically creates the database if it doesn't exist. """
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI.rsplit("/", 1)[0])  # Connect without DB name
    with engine.connect() as connection:
        db_name = Config.SQLALCHEMY_DATABASE_URI.rsplit("/", 1)[1]  # Extract DB name
        existing_databases = connection.execute(text("SHOW DATABASES;"))
        if db_name not in [row[0] for row in existing_databases]:
            connection.execute(text(f"CREATE DATABASE {db_name};"))
            print(f"Database '{db_name}' created successfully!")

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


