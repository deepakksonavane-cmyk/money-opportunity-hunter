from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from datetime import datetime


@dataclass
class Opportunity:
    """Real opportunity from actual sources."""
    project_client: str
    platform: str
    requirement: str
    payment: Optional[int]  # None = UNKNOWN
    estimated_days: Optional[int]  # None = UNKNOWN
    deadline: str
    application_url: str
    source_url: str
    posted_date: Optional[str] = None
    currency: str = "INR"
    status: str = "NEW"
    confidence: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    why_fit: str = ""
    recommended_bid: Optional[int] = None
    short_pitch: str = ""
    notes: str = ""
    # Scores
    fit_score: int = 0
    pay_score: int = 0
    time_score: int = 0
    credibility_score: int = 0
    win_score: int = 0
    overall_score: int = 0
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_client": self.project_client,
            "platform": self.platform,
            "requirement": self.requirement,
            "payment": self.payment,
            "estimated_days": self.estimated_days,
            "deadline": self.deadline,
            "application_url": self.application_url,
            "source_url": self.source_url,
            "posted_date": self.posted_date,
            "currency": self.currency,
            "status": self.status,
            "confidence": self.confidence,
            "why_fit": self.why_fit,
            "recommended_bid": self.recommended_bid,
            "short_pitch": self.short_pitch,
            "notes": self.notes,
            "fit_score": self.fit_score,
            "pay_score": self.pay_score,
            "time_score": self.time_score,
            "credibility_score": self.credibility_score,
            "win_score": self.win_score,
            "overall_score": self.overall_score,
        }
