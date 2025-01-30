# Configuration for database
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql://root:loki2001@localhost/healthcheck"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
