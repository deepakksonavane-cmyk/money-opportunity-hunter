from typing import List

from .models import Opportunity


def score_fit(opportunity: Opportunity) -> int:
    text = (opportunity.requirement + " " + opportunity.why_fit).lower()
    score = 0
    if "market" in text:
        score += 15
    if "research" in text or "intelligence" in text:
        score += 15
    if "feasibility" in text or "business model" in text:
        score += 15
    if "territory" in text or "vendor" in text:
        score += 15
    if "sponsorship" in text or "customer" in text:
        score += 15
    if "competitor" in text or "forecast" in text:
        score += 15
    if "operations" in text or "sop" in text:
        score += 10
    return min(score, 100)


def score_pay(payment: int) -> int:
    if payment < 10000:
        return 0
    if payment < 20000:
        return 40
    if payment < 35000:
        return 65
    if payment < 60000:
        return 80
    if payment < 90000:
        return 90
    return 100


def score_time(days: int) -> int:
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
    return 15


def score_credibility(platform: str) -> int:
    known = {
        "upwork": 80,
        "fiverr": 75,
        "linkedin jobs / consulting": 82,
        "peopleperhour": 78,
        "workana": 75,
        "ngo / csr portals": 68,
        "consulting": 72,
    }
    return known.get(platform.lower(), 65)


def score_win_probability(opportunity: Opportunity) -> int:
    score = 50
    text = opportunity.requirement.lower()
    if "market research" in text:
        score += 15
    if "territory" in text:
        score += 10
    if "vendor" in text:
        score += 8
    if "sponsorship" in text:
        score += 10
    if opportunity.estimated_days <= 7:
        score += 10
    if opportunity.payment >= 25000:
        score += 10
    return min(score, 100)


def build_bid(payment: int) -> int:
    if payment < 15000:
        return payment
    if payment < 30000:
        return int(payment * 0.72)
    if payment < 60000:
        return int(payment * 0.68)
    return int(payment * 0.62)


def generate_pitch(opportunity: Opportunity) -> str:
    return (
        "I can help you rapidly assess the opportunity, map the market, identify the right customer or partner segments, "
        "build a practical feasibility view, and turn it into a clear action plan with research-backed recommendations."
    )


def score_opportunity(opportunity: Opportunity) -> Opportunity:
    opportunity.fit_score = score_fit(opportunity)
    opportunity.pay_score = score_pay(opportunity.payment)
    opportunity.time_score = score_time(opportunity.estimated_days)
    opportunity.credibility_score = score_credibility(opportunity.platform)
    opportunity.win_score = score_win_probability(opportunity)
    opportunity.overall_score = round(
        0.30 * opportunity.fit_score
        + 0.20 * opportunity.pay_score
        + 0.20 * opportunity.time_score
        + 0.15 * opportunity.credibility_score
        + 0.15 * opportunity.win_score
    )
    opportunity.recommended_bid = build_bid(opportunity.payment)
    opportunity.short_pitch = generate_pitch(opportunity)
    return opportunity


def rank_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    scored = [score_opportunity(opp) for opp in opportunities]
    scored.sort(key=lambda x: x.overall_score, reverse=True)
    return scored
