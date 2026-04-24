import logging
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from app.external.hunter_client import HunterClient
from app.models.db import db
from app.models.lead import Lead
from app.models.query_log import QueryLog
from app.services.pitch_service import build_pitches

logger = logging.getLogger(__name__)


class LeadService:
    def __init__(self) -> None:
        self.hunter_client = HunterClient()

    def find_or_create_lead(self, company: str) -> dict[str, Any]:
        domain = self._normalize_domain(company)
        existing = Lead.query.filter_by(domain=domain).first()
        if existing:
            self._write_log(existing, status="cached")
            return existing.to_dict()

        result = self.hunter_client.find_best_email(domain)
        pitches = build_pitches(domain)

        lead = Lead(
            company=company,
            domain=domain,
            email=result.get("email"),
            confidence=result.get("confidence"),
            pitch=pitches["pitch"],
            short_pitch=pitches["short_pitch"],
        )

        try:
            db.session.add(lead)
            db.session.flush()
            self._write_log(lead, status="created")
            db.session.commit()
            return lead.to_dict()
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.exception("Failed to save lead domain=%s", domain)
            self._write_error_log(company, domain, str(exc))
            raise RuntimeError("Database write failed") from exc

    def process_batch(self, companies: list[str]) -> list[dict[str, Any]]:
        results = []
        for company in companies:
            try:
                results.append(
                    {
                        "company": company,
                        "status": "success",
                        "data": self.find_or_create_lead(company),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                logger.exception("Batch process failed for company=%s", company)
                results.append(
                    {
                        "company": company,
                        "status": "failed",
                        "error": str(exc),
                    }
                )
        return results

    @staticmethod
    def _normalize_domain(company: str) -> str:
        cleaned = company.strip().lower().replace("http://", "").replace("https://", "")
        return cleaned.split("/")[0]

    @staticmethod
    def _write_log(lead: Lead, status: str) -> None:
        log = QueryLog(
            company=lead.company,
            domain=lead.domain,
            email=lead.email,
            confidence=lead.confidence,
            pitch=lead.pitch,
            status=status,
        )
        db.session.add(log)

    @staticmethod
    def _write_error_log(company: str, domain: str, error_message: str) -> None:
        log = QueryLog(
            company=company,
            domain=domain,
            status="failed",
            error_message=error_message,
        )
        db.session.add(log)
        db.session.commit()
