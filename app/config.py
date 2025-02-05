# Configuration for database
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    DB_USER = os.getenv("DB_USER", "default_user")  # Default user (optional)
    DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")  # Default password (optional)

    # Static database host and name
    DB_HOST = "localhost"
    DB_NAME = "healthcheck"

    # Construct the SQLAlchemy Database URI dynamically
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
