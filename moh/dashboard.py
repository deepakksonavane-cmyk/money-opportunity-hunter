import csv
from typing import List
from .models import Opportunity


def print_dashboard(opportunities: List[Opportunity], top_n: int = 10):
    """Print a formatted dashboard of top opportunities."""
    rows = opportunities[:top_n]

    print("\n" + "="*140)
    print("MONEY OPPORTUNITY HUNTER - TOP 10 RANKED OPPORTUNITIES")
    print("="*140)
    print(
        f"{'Project':<30} {'Platform':<20} {'Pay':>12} {'Days':>6} {'Fit':>5} {'Score':>6} {'Conf':>6} {'Deadline':<15} {'Apply':<50}"
    )
    print("-" * 140)

    for i, opp in enumerate(rows, 1):
        pay_str = f"₹{opp.payment:,}" if opp.payment else "UNKNOWN"
        days_str = str(opp.estimated_days) if opp.estimated_days else "?"
        url = opp.application_url[:47] + "..." if len(opp.application_url) > 50 else opp.application_url

        print(
            f"{opp.project_client:<30} "
            f"{opp.platform:<20} "
            f"{pay_str:>12} "
            f"{days_str:>6} "
            f"{opp.fit_score:>5} "
            f"{opp.overall_score:>6} "
            f"{opp.confidence:>6} "
            f"{opp.deadline:<15} "
            f"{url:<50}"
        )

    print("\n" + "-" * 140)
    if rows:
        print(f"\nDETAILED VIEW OF TOP OPPORTUNITY:")
        top = rows[0]
        print(f"\n  Project: {top.project_client}")
        print(f"  Platform: {top.platform}")
        print(f"  Requirement: {top.requirement[:200]}..." if len(top.requirement) > 200 else f"  Requirement: {top.requirement}")
        print(f"  Payment: {f'₹{top.payment:,}' if top.payment else 'UNKNOWN'}")
        print(f"  Estimated days: {top.estimated_days if top.estimated_days else 'UNKNOWN'}")
        print(f"  Deadline: {top.deadline}")
        print(f"  Fit score: {top.fit_score}/100")
        print(f"  Overall score: {top.overall_score}/100")
        print(f"  Confidence: {top.confidence}")
        print(f"  Why it fits: {top.why_fit}")
        print(f"  Recommended bid: {f'₹{top.recommended_bid:,}' if top.recommended_bid else 'UNKNOWN'} (based on {top.payment})")
        print(f"  Apply: {top.application_url}")
        print(f"  Source: {top.source_url}")
    print()


def export_csv(opportunities: List[Opportunity], path: str):
    """Export opportunities to CSV file."""
    fieldnames = [
        "project_client",
        "platform",
        "requirement",
        "payment",
        "estimated_days",
        "deadline",
        "application_url",
        "source_url",
        "posted_date",
        "currency",
        "status",
        "confidence",
        "why_fit",
        "recommended_bid",
        "fit_score",
        "pay_score",
        "time_score",
        "credibility_score",
        "win_score",
        "overall_score",
    ]

    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for opp in opportunities:
            writer.writerow({
                "project_client": opp.project_client,
                "platform": opp.platform,
                "requirement": opp.requirement,
                "payment": opp.payment,
                "estimated_days": opp.estimated_days,
                "deadline": opp.deadline,
                "application_url": opp.application_url,
                "source_url": opp.source_url,
                "posted_date": opp.posted_date,
                "currency": opp.currency,
                "status": opp.status,
                "confidence": opp.confidence,
                "why_fit": opp.why_fit,
                "recommended_bid": opp.recommended_bid,
                "fit_score": opp.fit_score,
                "pay_score": opp.pay_score,
                "time_score": opp.time_score,
                "credibility_score": opp.credibility_score,
                "win_score": opp.win_score,
                "overall_score": opp.overall_score,
            })

    print(f"✓ Exported {len(opportunities)} opportunities to {path}")
