from typing import List, Optional
from .models import Opportunity


def score_fit(opportunity: Opportunity) -> int:
    """Score fit to Deepak's capabilities (0-100)."""
    text = (opportunity.requirement + " " + opportunity.why_fit).lower()
    score = 0

    # Each keyword adds points
    keywords_map = {
        "market research": 20,
        "feasibility": 20,
        "business model": 20,
        "customer discovery": 15,
        "territory": 18,
        "vendor research": 18,
        "competitor": 15,
        "sponsorship": 15,
        "forecasting": 12,
        "market intelligence": 15,
        "operations planning": 12,
        "sop": 10,
        "project planning": 12,
        "commercial analysis": 15,
    }

    for keyword, points in keywords_map.items():
        if keyword in text:
            score += points

    return min(100, score)


def score_pay(payment: Optional[int]) -> int:
    """Score payment (0-100). Unknown = 50."""
    if payment is None:
        return 50  # Unknown
    if payment < 10000:
        return 0
    if payment < 15000:
        return 30
    if payment < 20000:
        return 40
    if payment < 30000:
        return 60
    if payment < 50000:
        return 75
    if payment < 75000:
        return 85
    if payment < 100000:
        return 90
    return 100


def score_time(days: Optional[int]) -> int:
    """Score time requirement (0-100). Prefer fast completion. Unknown = 50."""
    if days is None:
        return 50  # Unknown
    if days <= 2:
        return 95
    if days <= 3:
        return 90
    if days <= 5:
        return 80
    if days <= 7:
        return 72
    if days <= 10:
        return 60
    if days <= 15:
        return 45
    return 0


def score_credibility(platform: str) -> int:
    """Score platform credibility (0-100)."""
    known_platforms = {
        "upwork": 90,
        "fiverr": 85,
        "freelancer": 80,
        "linkedin": 88,
        "peopleperhour": 78,
        "workana": 75,
        "guru": 72,
        "toptal": 95,
        "consulting marketplace": 70,
        "ngo": 65,
        "csr": 65,
    }

    platform_lower = platform.lower()
    for key, score in known_platforms.items():
        if key in platform_lower:
            return score

    return 60  # Unknown platform


def score_win_probability(opportunity: Opportunity) -> int:
    """Score likelihood of winning this opportunity (0-100)."""
    score = 50
    text = opportunity.requirement.lower()

    # Skill match
    if "market research" in text:
        score += 15
    if "territory" in text:
        score += 12
    if "vendor" in text:
        score += 10
    if "sponsorship" in text:
        score += 10
    if "feasibility" in text:
        score += 12
    if "business model" in text:
        score += 12

    # Timeline favor
    if opportunity.estimated_days is not None:
        if opportunity.estimated_days <= 5:
            score += 15
        elif opportunity.estimated_days <= 10:
            score += 8

    # Payment favor
    if opportunity.payment is not None:
        if opportunity.payment >= 30000:
            score += 10
        elif opportunity.payment >= 20000:
            score += 5

    # Platform credibility
    if opportunity.platform.lower() in ["upwork", "linkedin"]:
        score += 5

    return min(100, score)


def calculate_confidence(opportunity: Opportunity) -> str:
    """Determine confidence level based on data completeness."""
    missing = 0

    if opportunity.payment is None:
        missing += 1
    if opportunity.estimated_days is None:
        missing += 1
    if not opportunity.deadline or opportunity.deadline == "Unknown":
        missing += 1

    if missing == 0:
        return "HIGH"
    elif missing == 1:
        return "MEDIUM"
    else:
        return "LOW"


def build_bid(payment: Optional[int]) -> Optional[int]:
    """Calculate recommended bid based on budget."""
    if payment is None:
        return None
    if payment < 15000:
        return payment
    if payment < 30000:
        return int(payment * 0.72)
    if payment < 60000:
        return int(payment * 0.68)
    return int(payment * 0.62)


def generate_pitch(opportunity: Opportunity) -> str:
    """Generate a short pitch for this opportunity."""
    if opportunity.why_fit:
        return opportunity.why_fit[:150]
    return (
        "I can help you rapidly assess the opportunity, identify market dynamics, "
        "and build a clear action plan with research-backed recommendations."
    )


def score_opportunity(opportunity: Opportunity) -> Opportunity:
    """Score an opportunity and calculate all metrics."""
    opportunity.fit_score = score_fit(opportunity)
    opportunity.pay_score = score_pay(opportunity.payment)
    opportunity.time_score = score_time(opportunity.estimated_days)
    opportunity.credibility_score = score_credibility(opportunity.platform)
    opportunity.win_score = score_win_probability(opportunity)

    # Weighted overall score
    opportunity.overall_score = round(
        0.30 * opportunity.fit_score
        + 0.20 * opportunity.pay_score
        + 0.20 * opportunity.time_score
        + 0.15 * opportunity.credibility_score
        + 0.15 * opportunity.win_score
    )

    opportunity.recommended_bid = build_bid(opportunity.payment)
    opportunity.short_pitch = generate_pitch(opportunity)
    opportunity.confidence = calculate_confidence(opportunity)

    return opportunity


def rank_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    """Score and rank opportunities by overall score (descending)."""
    scored = [score_opportunity(opp) for opp in opportunities]
    scored.sort(key=lambda x: x.overall_score, reverse=True)
    return scored
