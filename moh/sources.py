import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from .models import Opportunity


class OpportunitySource:
    """Base class for opportunity sources."""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, url: str, timeout: int = 10) -> Optional[str]:
        """Fetch URL safely."""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  ⚠ Failed to fetch {url}: {str(e)[:60]}")
            return None

    def search(self) -> List[Opportunity]:
        """Override in subclass."""
        return []


class UpworkSource(OpportunitySource):
    """Upwork public job listings (no login required)."""

    def search(self) -> List[Opportunity]:
        print("  [*] Searching Upwork...")
        opportunities = []
        
        # Upwork search URLs for market research, feasibility, business model work
        search_terms = [
            "market research",
            "feasibility study",
            "business model",
            "territory research",
            "vendor research",
        ]

        for term in search_terms:
            url = f"https://www.upwork.com/nx/search/jobs?q={term}&sort=recency"
            html = self.fetch(url)
            if not html:
                continue

            # Note: Upwork has anti-scraping, this is a placeholder
            # Real implementation would use Upwork API with auth
            # For now, returning empty to indicate source needs API
        
        return opportunities


class FreelancerSource(OpportunitySource):
    """Freelancer.com public job listings."""

    def search(self) -> List[Opportunity]:
        print("  [*] Searching Freelancer...")
        opportunities = []
        
        # Freelancer.com search page
        url = "https://www.freelancer.com/jobs/research/"
        html = self.fetch(url)
        if not html:
            return opportunities

        # Placeholder: would parse job cards from HTML
        # Requires reverse-engineering HTML structure
        
        return opportunities


class LinkedInSource(OpportunitySource):
    """LinkedIn public job postings (no login required)."""

    def search(self) -> List[Opportunity]:
        print("  [*] Searching LinkedIn...")
        opportunities = []
        
        # LinkedIn job search
        url = "https://www.linkedin.com/jobs/search/?keywords=market%20research&location=India"
        html = self.fetch(url)
        if not html:
            return opportunities

        # Placeholder: would parse job listings
        # LinkedIn requires authentication for detailed scraping
        
        return opportunities


class PeoplePerHourSource(OpportunitySource):
    """PeoplePerHour public work postings."""

    def search(self) -> List[Opportunity]:
        print("  [*] Searching PeoplePerHour...")
        opportunities = []
        
        url = "https://www.peoplesperhour.com/"
        # Placeholder: would need HTML parsing
        
        return opportunities


class PublicJSONSource(OpportunitySource):
    """Load opportunities from a JSON file (for testing)."""

    def __init__(self, json_path: str):
        super().__init__()
        self.json_path = json_path

    def search(self) -> List[Opportunity]:
        print(f"  [*] Loading from {self.json_path}...")
        opportunities = []
        
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"  ⚠ File not found: {self.json_path}")
            return opportunities
        except json.JSONDecodeError:
            print(f"  ⚠ Invalid JSON: {self.json_path}")
            return opportunities

        opp_list = data if isinstance(data, list) else data.get("opportunities", [])
        
        for item in opp_list:
            try:
                opp = Opportunity(
                    project_client=item.get("project_client", "Unknown"),
                    platform=item.get("platform", "Unknown"),
                    requirement=item.get("requirement", ""),
                    payment=item.get("payment"),  # Can be None
                    estimated_days=item.get("estimated_days"),  # Can be None
                    deadline=item.get("deadline", "Unknown"),
                    application_url=item.get("application_url", ""),
                    source_url=item.get("source_url", item.get("application_url", "")),
                    posted_date=item.get("posted_date"),
                    currency=item.get("currency", "INR"),
                    status=item.get("status", "NEW"),
                    why_fit=item.get("why_fit", ""),
                    notes=item.get("notes", ""),
                )
                opportunities.append(opp)
                print(f"    ✓ {opp.project_client}")
            except Exception as e:
                print(f"    ⚠ Error parsing opportunity: {str(e)}")
                continue
        
        return opportunities


def search_opportunities(sources: Optional[List[OpportunitySource]] = None) -> List[Opportunity]:
    """Search all provided sources and return combined results."""
    if sources is None:
        sources = []

    all_opportunities = []

    for source in sources:
        try:
            opportunities = source.search()
            all_opportunities.extend(opportunities)
        except Exception as e:
            print(f"  ✗ Source error: {str(e)}")
            continue

    # Deduplicate by (client, platform, requirement, url)
    seen = set()
    unique = []
    
    for opp in all_opportunities:
        key = (
            opp.project_client.lower(),
            opp.platform.lower(),
            opp.requirement[:100].lower(),
            opp.application_url.lower(),
        )
        if key not in seen:
            seen.add(key)
            unique.append(opp)

    print(f"\n  ✓ Total opportunities found: {len(all_opportunities)}")
    print(f"  ✓ After deduplication: {len(unique)}")
    
    return unique
