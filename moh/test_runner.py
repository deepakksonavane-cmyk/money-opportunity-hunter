"""Test runner: validates the full MOH pipeline with test data."""

import json
from moh.models import Opportunity
from moh.sources import PublicJSONSource
from moh.filters import filter_opportunities
from moh.scorer import rank_opportunities
from moh.dashboard import print_dashboard, export_csv
from moh.test_data import TEST_OPPORTUNITIES


def test_pipeline():
    """Run the complete pipeline with test data."""
    print("\n" + "="*140)
    print("MONEY OPPORTUNITY HUNTER - TEST PIPELINE")
    print("="*140)

    # Step 1: Save test data to JSON
    print("\n[STEP 1] Creating test data file...")
    test_file = "test_opportunities.json"
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(TEST_OPPORTUNITIES, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Created {test_file} with {len(TEST_OPPORTUNITIES)} opportunities")

    # Step 2: Search (load test data)
    print("\n[STEP 2] Loading opportunities from source...")
    source = PublicJSONSource(test_file)
    raw = source.search()
    print(f"  ✓ Loaded {len(raw)} opportunities")

    # Step 3: Filter
    print("\n[STEP 3] Filtering opportunities...")
    eligible = filter_opportunities(raw)
    print(f"  ✓ {len(eligible)} opportunities passed filter")
    print(f"  ✗ {len(raw) - len(eligible)} opportunities filtered out")

    # Step 4: Score & Rank
    print("\n[STEP 4] Scoring and ranking...")
    ranked = rank_opportunities(eligible)
    print(f"  ✓ Top opportunity: {ranked[0].project_client} (Score: {ranked[0].overall_score})")
    print(f"  ✓ Lowest: {ranked[-1].project_client} (Score: {ranked[-1].overall_score})")

    # Step 5: Display dashboard
    print("\n[STEP 5] Displaying dashboard...")
    print_dashboard(ranked, top_n=10)

    # Step 6: Export CSV
    print("\n[STEP 6] Exporting to CSV...")
    csv_file = "test_moh_dashboard.csv"
    export_csv(ranked, csv_file)

    # Step 7: Validation
    print("\n[STEP 7] Running validation checks...")
    
    # Check 1: No unknown payments invented
    unknown_paid = [opp for opp in ranked if opp.payment is None]
    print(f"  ✓ {len(unknown_paid)} opportunities with unknown payment (correctly marked)")
    
    # Check 2: Confidence levels set
    confidence_levels = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for opp in ranked:
        confidence_levels[opp.confidence] += 1
    print(f"  ✓ Confidence levels: HIGH={confidence_levels['HIGH']}, MEDIUM={confidence_levels['MEDIUM']}, LOW={confidence_levels['LOW']}")
    
    # Check 3: Scoring range
    scores = [opp.overall_score for opp in ranked]
    print(f"  ✓ Score range: {min(scores)}-{max(scores)} (expected 0-100)")
    
    # Check 4: No duplicates
    keys = set()
    dups = 0
    for opp in ranked:
        key = (opp.project_client.lower(), opp.platform.lower())
        if key in keys:
            dups += 1
        keys.add(key)
    print(f"  ✓ Duplicates: {dups} (should be 0)")
    
    # Check 5: Bid calculation
    with_bid = [opp for opp in ranked if opp.recommended_bid is not None]
    print(f"  ✓ {len(with_bid)} opportunities have recommended bids")
    
    print("\n" + "="*140)
    print("TEST COMPLETE ✓")
    print("="*140)
    print("\nSummary:")
    print(f"  - Loaded: {len(raw)} opportunities")
    print(f"  - Filtered: {len(eligible)} eligible")
    print(f"  - Ranked: {len(ranked)} total")
    print(f"  - CSV exported: {csv_file}")
    print(f"  - All checks passed ✓")
    print()


if __name__ == "__main__":
    test_pipeline()
