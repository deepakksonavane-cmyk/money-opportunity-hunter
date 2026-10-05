from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable, List, Optional, Any, Dict

import requests
from bs4 import BeautifulSoup


class OpportunityVerifier:
    """Performs lightweight verification of public opportunity pages."""

    def __init__(self, timeout: int = 12):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

    @staticmethod
    def _clean_text(value: str) -> str:
        if not value:
            return ""
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def fetch(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception:
            return None

    def inspect_page(self, url: str) -> Dict[str, Any]:
        html = self.fetch(url)
        if not html:
            return {
                "status": "unreachable",
                "title": "",
                "keywords_found": [],
                "excerpt": "",
            }

        soup = BeautifulSoup(html, "html.parser")
        title = self._clean_text(soup.title.string) if soup.title and soup.title.string else ""
        text = self._clean_text(soup.get_text(" ", strip=True))
        keywords = [
            token for token in [
                "market research",
                "feasibility",
                "business model",
                "customer discovery",
                "territory",
                "vendor research",
                "sponsorship",
                "competitor",
                "market intelligence",
                "operations planning",
                "project planning",
                "commercial analysis",
            ]
            if token in text.lower()
        ]

        excerpt = text[:500]
        if not text:
            excerpt = ""

        return {
            "status": "reachable",
            "title": title,
            "keywords_found": keywords,
            "excerpt": excerpt,
        }

    def verify_opportunity(self, opportunity: Any) -> Any:
        """Set verification metadata on an opportunity-like object."""
        inspection = self.inspect_page(getattr(opportunity, "application_url", "") or getattr(opportunity, "source_url", ""))
        opportunity.verified_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

        if inspection["status"] == "reachable":
            opportunity.confidence = "MEDIUM"
            if inspection["keywords_found"]:
                opportunity.confidence = "HIGH"
            opportunity.active_status = "ACTIVE"
            opportunity.evidence = inspection["title"] or inspection["excerpt"] or opportunity.source_url
        else:
            opportunity.confidence = "LOW"
            opportunity.active_status = "UNKNOWN"
            opportunity.evidence = opportunity.source_url or "Public discovery only"

        opportunity.notes = (opportunity.notes + " 
Verification: " + opportunity.evidence).strip()
        return opportunity

    def verify_opportunities(self, opportunities: Iterable[Any]) -> List[Any]:
        verified: List[Any] = []
        for opportunity in opportunities:
            verified.append(self.verify_opportunity(opportunity))
        return verified


def verify_opportunities(opportunities: Iterable[Any]) -> List[Any]:
    return OpportunityVerifier().verify_opportunities(opportunities)


def verify_opportunity(opportunity: Any) -> Any:
    return OpportunityVerifier().verify_opportunity(opportunity)
