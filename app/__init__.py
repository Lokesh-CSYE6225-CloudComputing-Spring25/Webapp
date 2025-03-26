# Flask app factory
from flask import Flask, make_response
from .routes import app as flask_app  # Import the Flask instance from routes.py
from .models import db
from datetime import datetime, timezone
from app.config import Config
from sqlalchemy import create_engine, text
import os
import logging
import time
from pythonjsonlogger.jsonlogger import JsonFormatter
from logging.handlers import RotatingFileHandler

IS_TESTING = os.getenv("IS_TESTING") == "1"

if os.name == 'posix' and not IS_TESTING:
    LOG_DIR = "/var/log/csye6225"
else:
    LOG_DIR = "./logs"

LOG_FILE = os.path.join(LOG_DIR, "webapp.log")

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Structured JSON Logging Setup
class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))

formatter = CustomJsonFormatter()
formatter.default_time_format = '%Y-%m-%dT%H:%M:%SZ'

json_log_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
json_log_handler.setFormatter(formatter)

logger = logging.getLogger("csye6225")
logger.setLevel(logging.INFO)

# Avoid duplicate log entries
if not logger.handlers:
    logger.addHandler(json_log_handler)

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
    app = flask_app  # Use the existing Flask app from routes.py
    app.config.from_object(Config)  # Load config settings from Config class
    db.init_app(app)  # Initialize the database
    logger.info("Flask app initialized successfully.")
    # Ensure database exists before creating tables
    create_database()

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error=None):
        logger.warning("404 Not Found")
        response = make_response("", 404)
        return add_common_headers(response)

    @app.errorhandler(405)
    def method_not_allowed(error=None):
        logger.warning("405 Method Not Allowed")
        response = make_response("", 405)
        return add_common_headers(response)

    @app.errorhandler(500)
    def internal_server_error(error=None):
        logger.exception("Internal Server Error occurred")
        response = make_response("", 500)
        return add_common_headers(response)

    return app
