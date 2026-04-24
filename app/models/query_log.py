from datetime import datetime

from app.models.db import db


class QueryLog(db.Model):
    __tablename__ = "query_logs"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    company = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    pitch = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company": self.company,
            "domain": self.domain,
            "email": self.email,
            "confidence": self.confidence,
            "pitch": self.pitch,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
