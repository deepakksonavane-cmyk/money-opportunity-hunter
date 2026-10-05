import re
from typing import List

from .models import Opportunity

GOOD_KEYWORDS = [
    "market research",
    "feasibility",
    "business model",
    "customer discovery",
    "territory",
    "vendor research",
    "opportunity mapping",
    "sponsorship",
    "competitor",
    "forecasting",
    "market intelligence",
    "operations planning",
    "sop",
    "project planning",
    "commercial analysis",
]

DISQUALIFIERS = [
    "data entry",
    "virtual assistant",
    "admin support",
    "copy paste",
    "excel data scraping",
    "mlm",
    "network marketing",
    "unpaid internship",
    "generic va",
    "scam",
    "cold calling",
    "telemarketing",
    "recruitment agency",
    "months long commitment",
]


def contains_disqualifier(text: str) -> bool:
    text_l = text.lower()
    return any(token in text_l for token in DISQUALIFIERS)


def is_positive_fit(text: str) -> bool:
    text_l = text.lower()
    return any(keyword in text_l for keyword in GOOD_KEYWORDS)


def is_eligible(opportunity: Opportunity) -> bool:
    if not opportunity.requirement or not opportunity.project_client:
        return False
    if opportunity.payment < 10000:
        return False
    if opportunity.estimated_days > 15:
        return False
    if contains_disqualifier(opportunity.requirement):
        return False
    if not is_positive_fit(opportunity.requirement):
        return False
    return True


def filter_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    return [opp for opp in opportunities if is_eligible(opp)]
