import re
from urllib.parse import quote_plus
from typing import Iterable, List, Optional, Dict, Any

import requests
from bs4 import BeautifulSoup


DEFAULT_SEARCH_QUERIES = [
    "market research freelancer India",
    "feasibility study freelancer India",
    "business model consulting project India",
    "customer discovery research project India",
    "territory research opportunity India",
    "vendor research consultant India",
    "sponsorship strategy research India",
]


class PublicWebSearch:
    """Simple public web discovery layer that works without API keys."""

    def __init__(self, timeout: int = 12):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

    def _fetch(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # pragma: no cover - defensive
            print(f"  ⚠ Search fetch failed for {url}: {exc}")
            return None

    @staticmethod
    def _clean_text(value: str) -> str:
        if not value:
            return ""
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def _parse_duckduckgo_results(self, html: str) -> List[Dict[str, str]]:
        results: List[Dict[str, str]] = []
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a.result-link"):
            href = a.get("href") or ""
            title = self._clean_text(a.get_text(" ", strip=True))
            if href and title:
                results.append({"title": title, "url": href})
        return results

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search public web using DuckDuckGo HTML search."""
        encoded = quote_plus(query)
        url = f"https://duckduckgo.com/html/?q={encoded}"
        html = self._fetch(url)
        if not html:
            return []
        results = self._parse_duckduckgo_results(html)
        deduped: List[Dict[str, str]] = []
        seen = set()
        for item in results:
            normalized = item["url"]
            if normalized not in seen:
                seen.add(normalized)
                deduped.append(item)
            if len(deduped) >= max_results:
                break
        return deduped

    def search_queries(self, queries: Optional[Iterable[str]] = None, max_results: int = 5) -> List[Dict[str, str]]:
        queries = list(queries or DEFAULT_SEARCH_QUERIES)
        merged: List[Dict[str, str]] = []
        seen = set()
        for query in queries:
            for result in self.search(query, max_results=max_results):
                key = result["url"]
                if key not in seen:
                    seen.add(key)
                    merged.append(result)
        return merged


def build_default_search_queries() -> List[str]:
    return list(DEFAULT_SEARCH_QUERIES)


def discover_public_links(
    queries: Optional[Iterable[str]] = None,
    max_results_per_query: int = 5,
) -> List[Dict[str, str]]:
    searcher = PublicWebSearch()
    return searcher.search_queries(queries=queries, max_results=max_results_per_query)


def discover_public_opportunities(
    queries: Optional[Iterable[str]] = None,
    max_results_per_query: int = 5,
) -> List[Dict[str, Any]]:
    """Return a list of public opportunity candidates keyed by discovered URLs."""
    links = discover_public_links(
        queries=queries,
        max_results_per_query=max_results_per_query,
    )

    opportunities: List[Dict[str, Any]] = []
    for index, item in enumerate(links):
        url = item.get("url", "")
        title = item.get("title", "")
        opportunities.append(
            {
                "project_client": title or "Public Web Listing",
                "platform": "Public Web",
                "requirement": title,
                "payment": None,
                "estimated_days": None,
                "deadline": "Unknown",
                "application_url": url,
                "source_url": url,
                "status": "NEW",
                "why_fit": "Public web discovery candidate requiring verification.",
                "notes": f"Discovered via public search result #{index + 1}.",
                "confidence": "LOW",
                "active_status": "UNKNOWN",
                "raw": item,
            }
        )
    return opportunities


if __name__ == "__main__":
    sample = discover_public_opportunities(max_results_per_query=3)
    for item in sample[:5]:
        print(item["project_client"], "->", item["application_url"])
