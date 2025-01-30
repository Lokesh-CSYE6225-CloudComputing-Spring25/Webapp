# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Initialize db here

class HealthCheck(db.Model):
    __tablename__ = "health_check"  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


