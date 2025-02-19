import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME")

    # Ensure all required variables are loaded
    if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
        raise ValueError("ERROR: Missing required database environment variables!")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
