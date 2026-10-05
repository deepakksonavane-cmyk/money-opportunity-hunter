from pathlib import Path

from .sources import search_opportunities, PublicJSONSource, OpportunitySource
from .web_search import discover_public_opportunities
from .verification import verify_opportunities
from .filters import filter_opportunities
from .scorer import rank_opportunities
from .dashboard import print_dashboard, export_csv


def run(
    sources=None,
    json_path=None,
    top_n=10,
    output_csv="moh_dashboard.csv",
):
    """Public-web-aware runner.

    Preserves the existing local pipeline but adds a public-web discovery and
    verification layer when no explicit sources are supplied.
    """
    print("\n" + "=" * 80)
    print("MONEY OPPORTUNITY HUNTER")
    print("=" * 80)

    if json_path:
        sources = [PublicJSONSource(json_path)]

    if sources is None or len(sources) == 0:
        print("\n[DISCOVER] Searching public web for active opportunity candidates...")
        discovered = discover_public_opportunities(max_results_per_query=5)
        if discovered:
            verified = verify_opportunities(discovered)
            raw = verified
            print(f"  Result: {len(raw)} public-web candidates discovered and verified")
        else:
            print("  No public-web candidates discovered.")
            raw = []
    else:
        print("\n[SEARCH] Finding opportunities...")
        raw = search_opportunities(sources)
        print(f"  Result: {len(raw)} opportunities found")

    if not raw:
        print("\n  ✗ No opportunities matched your search. Try different keywords.")
        return []

    print("\n[FILTER] Checking eligibility...")
    eligible = filter_opportunities(raw)
    filtered_out = len(raw) - len(eligible)
    print(f"  Result: {len(eligible)} passed filter")
    if filtered_out > 0:
        print(f"         {filtered_out} rejected (not matching profile)")

    if not eligible:
        print("\n  ✗ No opportunities matched your profile. Try different sources.")
        return []

    print("\n[SCORE] Calculating fit scores...")
    ranked = rank_opportunities(eligible)
    print(f"  Result: {len(ranked)} opportunities ranked")

    print("\n[DISPLAY] Top opportunities:")
    print_dashboard(ranked, top_n=top_n)

    print("\n[EXPORT] Saving results...")
    export_csv(ranked, output_csv)

    print("\n" + "=" * 80)
    return ranked


if __name__ == "__main__":
    run(top_n=10)
