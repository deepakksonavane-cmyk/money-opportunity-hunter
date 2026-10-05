from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class Opportunity:
    project_client: str
    platform: str
    requirement: str
    payment: int
    estimated_days: int
    why_fit: str
    deadline: str
    application_url: str
    status: str = "NEW"
    recommended_bid: Optional[int] = None
    short_pitch: Optional[str] = None
    notes: str = ""
    fit_score: int = 0
    pay_score: int = 0
    time_score: int = 0
    credibility_score: int = 0
    win_score: int = 0
    overall_score: int = 0
    source_url: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_client": self.project_client,
            "platform": self.platform,
            "requirement": self.requirement,
            "payment": self.payment,
            "estimated_days": self.estimated_days,
            "why_fit": self.why_fit,
            "deadline": self.deadline,
            "application_url": self.application_url,
            "status": self.status,
            "recommended_bid": self.recommended_bid,
            "short_pitch": self.short_pitch,
            "notes": self.notes,
            "fit_score": self.fit_score,
            "pay_score": self.pay_score,
            "time_score": self.time_score,
            "credibility_score": self.credibility_score,
            "win_score": self.win_score,
            "overall_score": self.overall_score,
            "source_url": self.source_url,
        }
