# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()  # Initialize db here

class HealthCheck(db.Model):
    __tablename__ = "health_check"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)



