import logging
import os
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class HunterClient:
    BASE_URL = "https://api.hunter.io/v2/domain-search"

    def __init__(self) -> None:
        self.api_key = os.getenv("HUNTER_API_KEY", "")
        self.timeout = int(os.getenv("HTTP_TIMEOUT", "10"))
        self.max_retries = int(os.getenv("HUNTER_MAX_RETRIES", "2"))
        self.retry_backoff = float(os.getenv("HUNTER_RETRY_BACKOFF", "1.5"))

    def find_best_email(self, domain: str) -> dict:
        if not self.api_key:
            raise ValueError("HUNTER_API_KEY is not configured")

        params = {"domain": domain, "api_key": self.api_key, "limit": 1}
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
                response.raise_for_status()
                payload = response.json()
                return self._parse_response(payload)
            except requests.RequestException as exc:
                last_exception = exc
                logger.warning(
                    "Hunter request failed for domain=%s attempt=%s error=%s",
                    domain,
                    attempt + 1,
                    str(exc),
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff**attempt)

        raise RuntimeError(f"Hunter API request failed after retries: {last_exception}")

    @staticmethod
    def _parse_response(payload: dict) -> dict:
        data = payload.get("data", {})
        emails = data.get("emails", [])
        if not emails:
            return {"email": None, "confidence": None}

        first = emails[0]
        return {
            "email": first.get("value"),
            "confidence": (first.get("confidence") or 0) / 100,
        }
