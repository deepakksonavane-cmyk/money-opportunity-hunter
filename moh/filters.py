import json
import re
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .models import Opportunity

SEED_OPPORTUNITIES = [
    {
        "project_client": "SME Exporter Expansion",
        "platform": "LinkedIn Jobs / Consulting",
        "requirement": "Research 3 export markets, identify buyer segments, assess demand, build territory map, and prepare feasibility summary for B2B expansion.",
        "payment": 45000,
        "estimated_days": 7,
        "why_fit": "Strong in market research, territory mapping, opportunity intelligence, and business feasibility.",
        "deadline": "Within 72 hours",
        "application_url": "https://www.linkedin.com/jobs",
        "source_url": "https://www.linkedin.com/jobs",
        "status": "NEW",
    },
    {
        "project_client": "Sponsorship Growth Consultant",
        "platform": "Upwork",
        "requirement": "Create event sponsorship prospect list, draft sponsor deck, identify relevant brands, and estimate outreach strategy for a city event.",
        "payment": 28000,
        "estimated_days": 5,
        "why_fit": "Experienced in event project development, sponsorship, prospect mapping, and commercial storytelling.",
        "deadline": "Open now",
        "application_url": "https://www.upwork.com",
        "source_url": "https://www.upwork.com",
        "status": "NEW",
    },
    {
        "project_client": "Business Model Validation",
        "platform": "Fiverr / Consulting",
        "requirement": "Review startup idea, identify customer segments, build a simple business model canvas, assess pricing, competitors, and launch assumptions.",
        "payment": 22000,
        "estimated_days": 6,
        "why_fit": "Strong at business-model design, customer discovery, competitor research, and turning vague ideas into executable plans.",
        "deadline": "Open now",
        "application_url": "https://www.fiverr.com",
        "source_url": "https://www.fiverr.com",
        "status": "NEW",
    },
    {
        "project_client": "Regional Vendor Research",
        "platform": "Workana",
        "requirement": "Compile vendor shortlist for packaging, print, transport, and local service providers across 2 cities and compare costs and lead times.",
        "payment": 18000,
        "estimated_days": 4,
        "why_fit": "Excellent at vendor research, operations planning, SOP design, and commercial evaluation.",
        "deadline": "Open now",
        "application_url": "https://www.workana.com",
        "source_url": "https://www.workana.com",
        "status": "NEW",
    },
    {
        "project_client": "CSR / NGO Opportunity Mapping",
        "platform": "NGO / CSR portals",
        "requirement": "Map likely CSR-partner sectors, identify donor prospects, prepare an opportunity brief, and draft outreach notes for a social-impact initiative.",
        "payment": 35000,
        "estimated_days": 8,
        "why_fit": "Aligns with market intelligence, opportunity mapping, stakeholder research, and documentation.",
        "deadline": "Within 7 days",
        "application_url": "https://example.org/csr-opportunities",
        "source_url": "https://example.org/csr-opportunities",
        "status": "NEW",
    },
    {
        "project_client": "Territory Expansion Study",
        "platform": "PeoplePerHour",
        "requirement": "Research 5 target territories, find customer density, competitor presence, pricing models, and local partner opportunities for a new service business.",
        "payment": 30000,
        "estimated_days": 7,
        "why_fit": "Highly aligned with territory research, market intelligence, forecasting, and feasibility analysis.",
        "deadline": "Open now",
        "application_url": "https://www.peopleperhour.com",
        "source_url": "https://www.peopleperhour.com",
        "status": "NEW",
    },
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


def clean_text(value: str) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def load_seed_opportunities() -> List[Opportunity]:
    opportunities = []
    for item in SEED_OPPORTUNITIES:
        opportunities.append(
            Opportunity(
                project_client=item["project_client"],
                platform=item["platform"],
                requirement=item["requirement"],
                payment=int(item["payment"]),
                estimated_days=int(item["estimated_days"]),
                why_fit=item["why_fit"],
                deadline=item["deadline"],
                application_url=item["application_url"],
                status=item.get("status", "NEW"),
                source_url=item.get("source_url", item["application_url"]),
                notes=item.get("notes", ""),
            )
        )
    return opportunities


def fetch_public_page(url: str) -> Optional[str]:
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
    except Exception:
        return None


def extract_opportunities_from_html(html: str, source_name: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    lines = [line.strip() for line in re.split(r"\n+|\.|\;|\||\s{2,}", text) if line.strip()]
    opportunities = []
    for line in lines:
        if not line:
            continue
        if any(keyword in line.lower() for keyword in [
            "market",
            "research",
            "feasibility",
            "vendor",
            "sponsorship",
            "opportunity",
            "territory",
            "business model",
            "customer",
            "analysis",
            "competitor",
        ]):
            opportunities.append({
                "project_client": source_name,
                "platform": source_name,
                "requirement": line[:220],
                "payment": 25000,
                "estimated_days": 7,
                "why_fit": "Research and business analysis fit.",
                "deadline": "Open now",
                "application_url": "",
                "source_url": "",
                "status": "NEW",
            })
    return opportunities


def load_json_file(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("opportunities", [])
    except Exception:
        return []
    return []


def search_opportunities(source_urls: Optional[List[str]] = None, json_path: Optional[str] = None) -> List[Opportunity]:
    opportunities: List[Opportunity] = load_seed_opportunities()

    if json_path:
        for entry in load_json_file(json_path):
            opportunities.append(
                Opportunity(
                    project_client=entry.get("project_client", "Unknown"),
                    platform=entry.get("platform", "Unknown"),
                    requirement=entry.get("requirement", ""),
                    payment=int(entry.get("payment", 15000)),
                    estimated_days=int(entry.get("estimated_days", 7)),
                    why_fit=entry.get("why_fit", "Fits research and business development."),
                    deadline=entry.get("deadline", "Open now"),
                    application_url=entry.get("application_url", ""),
                    status=entry.get("status", "NEW"),
                    source_url=entry.get("source_url", entry.get("application_url", "")),
                    notes=entry.get("notes", ""),
                )
            )

    if source_urls:
        for url in source_urls:
            html = fetch_public_page(url)
            if html is None:
                continue
            discovered = extract_opportunities_from_html(html, source_name=url)
            for item in discovered:
                opportunities.append(
                    Opportunity(
                        project_client=item["project_client"],
                        platform=item["platform"],
                        requirement=item["requirement"],
                        payment=int(item["payment"]),
                        estimated_days=int(item["estimated_days"]),
                        why_fit=item["why_fit"],
                        deadline=item["deadline"],
                        application_url=item["application_url"],
                        source_url=url,
                        status=item["status"],
                    )
                )

    seen = set()
    deduped = []
    for opp in opportunities:
        key = (opp.project_client.lower(), opp.platform.lower(), opp.requirement.lower(), opp.application_url.lower())
        if key not in seen:
            seen.add(key)
            deduped.append(opp)
    return deduped
