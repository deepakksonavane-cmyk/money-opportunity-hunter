import re
from typing import List, Optional
from .models import Opportunity

DISQUALIFIERS = [
    "data entry",
    "virtual assistant",
    "admin support",
    "copy paste",
    "excel data scraping",
    "mlm",
    "network marketing",
    "unpaid internship",
    "unpaid",
    "generic va",
    "scam",
    "cold calling",
    "telemarketing",
    "recruitment agency",
    "months long commitment",
    "long term commitment",
]

GOOD_KEYWORDS = [
    "market research",
    "feasibility",
    "business model",
    "customer discovery",
    "territory mapping",
    "territory research",
    "vendor research",
    "competitor analysis",
    "competitor research",
    "opportunity mapping",
    "sponsorship",
    "business development",
    "forecasting",
    "market intelligence",
    "operations planning",
    "sop",
    "project planning",
    "commercial analysis",
    "market analysis",
    "feasibility study",
]


def contains_disqualifier(text: str) -> bool:
    """Check if text contains disqualifying keywords."""
    if not text:
        return False
    text_lower = text.lower()
    return any(token in text_lower for token in DISQUALIFIERS)


def is_positive_fit(text: str) -> bool:
    """Check if text contains good keywords matching Deepak's profile."""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in GOOD_KEYWORDS)


def is_eligible(opportunity: Opportunity) -> bool:
    """Check if opportunity meets minimum criteria."""
    # Required fields
    if not opportunity.requirement or not opportunity.project_client:
        return False

    # Payment check: if known, must be >= 10k
    if opportunity.payment is not None and opportunity.payment < 10000:
        return False

    # Duration check: if known, must be <= 15 days
    if opportunity.estimated_days is not None and opportunity.estimated_days > 15:
        return False

    # Disqualifiers
    if contains_disqualifier(opportunity.requirement):
        return False

    # Must have at least one good keyword
    if not is_positive_fit(opportunity.requirement):
        return False

    return True


def filter_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    """Filter opportunities to only eligible ones."""
    return [opp for opp in opportunities if is_eligible(opp)]
