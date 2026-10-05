"""Core data models for MOH."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List
from datetime import datetime
from enum import Enum


class ConfidenceLevel(Enum):
    """Verification confidence levels."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ActiveStatus(Enum):
    """Opportunity active status."""
    ACTIVE = "ACTIVE"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class PriorityLevel(Enum):
    """Application priority based on fit and commercial value."""
    APPLY_NOW = "🔥 APPLY NOW"
    GOOD = "🟢 GOOD"
    POSSIBLE = "🟡 POSSIBLE"
    SKIP = "🔴 SKIP"


@dataclass
class Opportunity:
    """Real verified opportunity from actual sources."""
    
    # Core fields
    project_client: str  # Client/company name or "Unknown"
    platform: str  # Where discovered: Upwork, Freelancer, LinkedIn, etc.
    requirement: str  # Actual project description
    payment: Optional[int]  # Budget amount or None for UNKNOWN
    estimated_days: Optional[int]  # Duration or None for UNKNOWN
    deadline: str  # Deadline or "Unknown"
    application_url: str  # Where to apply
    source_url: str  # Where discovered
    
    # Metadata
    posted_date: Optional[str] = None  # When posted
    currency: str = "INR"
    status: str = "NEW"
    confidence: str = "MEDIUM"  # HIGH, MEDIUM, LOW (verification confidence)
    active_status: str = "ACTIVE"  # ACTIVE, STALE, EXPIRED, UNKNOWN
    
    # Freshness tracking
    discovered_at: Optional[str] = None
    verified_at: Optional[str] = None
    freshness_days: Optional[int] = None
    
    # Fit & scoring
    why_fit: str = ""
    fit_score: int = 0
    pay_score: int = 0
    time_score: int = 0
    credibility_score: int = 0
    win_score: int = 0
    overall_score: int = 0
    
    # Application
    recommended_bid: Optional[int] = None
    short_pitch: str = ""
    application_pitch: str = ""
    
    # Evidence
    evidence: str = ""  # Source of truth for this opportunity
    
    # Metadata
    notes: str = \"\"\n    priority: str = \"🟡 POSSIBLE\"\n    raw: Dict[str, Any] = field(default_factory=dict)\n\n    def to_dict(self) -> Dict[str, Any]:\n        return {\n            \"project_client\": self.project_client,\n            \"platform\": self.platform,\n            \"requirement\": self.requirement,\n            \"payment\": self.payment,\n            \"estimated_days\": self.estimated_days,\n            \"deadline\": self.deadline,\n            \"application_url\": self.application_url,\n            \"source_url\": self.source_url,\n            \"posted_date\": self.posted_date,\n            \"currency\": self.currency,\n            \"status\": self.status,\n            \"confidence\": self.confidence,\n            \"active_status\": self.active_status,\n            \"why_fit\": self.why_fit,\n            \"fit_score\": self.fit_score,\n            \"pay_score\": self.pay_score,\n            \"time_score\": self.time_score,\n            \"credibility_score\": self.credibility_score,\n            \"win_score\": self.win_score,\n            \"overall_score\": self.overall_score,\n            \"recommended_bid\": self.recommended_bid,\n            \"priority\": self.priority,\n            \"evidence\": self.evidence,\n        }\n\n\n@dataclass\nclass DiscoveryResult:\n    \"\"\"Result of a discovery attempt.\"\"\"\n    source: str\n    status: str  # SUCCESS, BLOCKED, ERROR, EMPTY\n    candidates_found: int = 0\n    candidates_verified: int = 0\n    error_message: str = \"\"\n    error_timestamp: Optional[str] = None\n    opportunities: List[Opportunity] = field(default_factory=list)\n\n\n@dataclass\nclass PipelineReport:\n    \"\"\"Full pipeline execution report.\"\"\"\n    timestamp: str\n    discovery_results: List[DiscoveryResult] = field(default_factory=list)\n    total_discovered: int = 0\n    total_verified: int = 0\n    total_after_filter: int = 0\n    total_after_score: int = 0\n    top_10: List[Opportunity] = field(default_factory=list)\n    failures: List[str] = field(default_factory=list)\n    success: bool = False\n