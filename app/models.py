from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    aspect = db.Column(db.String(50), nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
