from datetime import datetime

from app.models.db import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    company = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    pitch = db.Column(db.Text, nullable=True)
    short_pitch = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company": self.company,
            "domain": self.domain,
            "email": self.email,
            "confidence": self.confidence,
            "pitch": self.pitch,
            "short_pitch": self.short_pitch,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
