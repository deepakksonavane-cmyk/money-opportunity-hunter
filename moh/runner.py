from .sources import search_opportunities, PublicJSONSource
from .filters import filter_opportunities
from .scorer import rank_opportunities
from .dashboard import print_dashboard, export_csv
from typing import Optional, List
from .sources import OpportunitySource


def run(
    sources: Optional[List[OpportunitySource]] = None,
    json_path: Optional[str] = None,
    top_n: int = 10,
    output_csv: str = "moh_dashboard.csv",
):
    """Main MOH pipeline: search → filter → score → rank → display.

    Args:
        sources: List of OpportunitySource objects to search
        json_path: Path to JSON file with opportunities (for testing)
        top_n: Number of top opportunities to display
        output_csv: CSV filename for export

    Returns:
        List of ranked opportunities
    """
    print("\n" + "="*80)
    print("MONEY OPPORTUNITY HUNTER")
    print("="*80)

    # Step 1: Search
    print("\n[SEARCH] Finding opportunities...")
    if json_path:
        sources = [PublicJSONSource(json_path)]
    if sources is None:
        sources = []
        print("  ⚠ No sources provided. Use: run(sources=[...])")

    raw = search_opportunities(sources)
    print(f"  Result: {len(raw)} opportunities found")

    # Step 2: Filter
    print("\n[FILTER] Checking eligibility...")
    eligible = filter_opportunities(raw)
    filtered_out = len(raw) - len(eligible)
    print(f"  Result: {len(eligible)} passed filter")
    if filtered_out > 0:
        print(f"         {filtered_out} rejected (not matching profile)")

    if not eligible:
        print("\n  ✗ No opportunities matched your profile. Try different sources.")
        return []

    # Step 3: Score & Rank
    print("\n[SCORE] Calculating fit scores...")
    ranked = rank_opportunities(eligible)
    print(f"  Result: {len(ranked)} opportunities ranked")

    # Step 4: Display
    print("\n[DISPLAY] Top opportunities:")
    print_dashboard(ranked, top_n=top_n)

    # Step 5: Export
    print("\n[EXPORT] Saving results...")
    export_csv(ranked, output_csv)

    print("\n" + "="*80)
    return ranked


if __name__ == "__main__":
    # Example: run with a JSON file
    run(json_path="opportunities.json", top_n=10)
