# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()  # Initialize db here

class HealthCheck(db.Model):
    __tablename__ = "health_check"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class FileMetadata(db.Model):
    __tablename__ = "files_metadata"
    id = db.Column(db.String(36), primary_key=True)  # UUID as primary key
    filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(512), unique=True, nullable=False)  # S3 path
    s3_url = db.Column(db.String(1024), nullable=False)  # Public URL
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
