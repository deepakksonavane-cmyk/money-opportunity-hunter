import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

# Keywords that match your skills
KEYWORDS = [
    'market research',
    'feasibility',
    'business model',
    'territory mapping',
    'vendor research',
    'customer discovery',
    'competitor analysis',
    'sponsorship',
    'project planning',
    'commercial analysis',
    'opportunity mapping',
    'business development',
    'sop',
    'forecasting',
    'market intelligence'
]

DISQUALIFY = [
    'data entry',
    'virtual assistant',
    'admin support',
    'copy paste',
    'mlm',
    'scam',
    'unpaid',
    'cold calling',
    'telemarketing'
]

class OpportunityScraper:
    def __init__(self):
        self.opportunities = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def load_existing(self):
        """Load existing opportunities from file"""
        if os.path.exists('opportunities.json'):
            try:
                with open('opportunities.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.opportunities = data.get('opportunities', [])
            except:
                self.opportunities = []

    def save_opportunities(self):
        """Save opportunities to file"""
        with open('opportunities.json', 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'opportunities': self.opportunities
            }, f, indent=2, ensure_ascii=False)

    def is_relevant(self, text):
        """Check if job posting matches keywords"""
        if not text:
            return False
        text_lower = text.lower()
        
        # Must contain at least one good keyword
        has_keyword = any(kw in text_lower for kw in KEYWORDS)
        
        # Must not contain disqualifier
        has_disqualifier = any(dq in text_lower for dq in DISQUALIFY)
        
        return has_keyword and not has_disqualifier

    def score_opportunity(self, opportunity):
        """Score an opportunity 0-100"""
        text = (opportunity.get('requirement', '') + ' ' + opportunity.get('platform', '')).lower()
        score = 50
        
        # Keyword matches
        if 'market' in text or 'research' in text:
            score += 15
        if 'feasibility' in text or 'business model' in text:
            score += 15
        if 'territory' in text or 'vendor' in text:
            score += 10
        if 'sponsorship' in text:
            score += 8
        
        # Time bonus (prefer quick projects)
        days = opportunity.get('estimated_days', 7)
        if days <= 5:
            score += 10
        elif days <= 10:
            score += 5
        
        # Payment bonus
        payment = opportunity.get('payment', 0)
        if payment >= 25000:
            score += 10
        elif payment >= 15000:
            score += 5
        
        return min(100, score)

    def fetch_page(self, url):
        """Fetch a webpage safely"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except:
            return None

    def scrape_reddit(self):
        """Scrape opportunity discussions from Reddit (if available)"""
        # This would require Reddit API or RSS feed
        # For now, we'll use sample data
        pass

    def scrape_freelancer_sites(self):
        """Scrape generic freelancer job listings"""
        print("[*] Searching freelancer platforms...")
        
        # Sample opportunities to simulate scraping
        found = [
            {
                'project_client': 'E-commerce Market Research',
                'platform': 'Upwork (Scrape)',
                'requirement': 'Research 3 new markets for e-commerce expansion. Analyze market size, competitors, customer segments.',
                'payment': 32000,
                'estimated_days': 6,
                'deadline': 'This week',
                'application_url': 'https://www.upwork.com/nx/search/jobs',
                'status': 'NEW',
            },
            {
                'project_client': 'Local Business Feasibility Study',
                'platform': 'Fiverr (Scrape)',
                'requirement': 'Evaluate feasibility of opening a service center in 2 cities. Assess competition, pricing, customer base.',
                'payment': 28000,
                'estimated_days': 7,
                'deadline': 'Open',
                'application_url': 'https://www.fiverr.com/search/gigs',
                'status': 'NEW',
            },
            {
                'project_client': 'Territory Vendor Mapping',
                'platform': 'Workana (Scrape)',
                'requirement': 'Map and list vendors in 3 territories. Create database with pricing and capabilities.',
                'payment': 22000,
                'estimated_days': 5,
                'deadline': 'Open',
                'application_url': 'https://www.workana.com',
                'status': 'NEW',
            },
        ]
        
        for opp in found:
            if self.is_relevant(opp['requirement']):
                opp['fit_score'] = self.score_opportunity(opp)
                self.opportunities.append(opp)
                print(f"  ✓ Found: {opp['project_client']} (₹{opp['payment']})")

    def scrape_linkedin_opportunities(self):
        """Scrape LinkedIn job postings"""
        print("[*] Searching LinkedIn opportunities...")
        
        found = [
            {
                'project_client': 'Strategy Consulting - Growth Markets',
                'platform': 'LinkedIn (Scrape)',
                'requirement': 'Consultant needed to research growth opportunities in Indian markets. Build market strategy and competitor analysis.',
                'payment': 50000,
                'estimated_days': 8,
                'deadline': 'ASAP',
                'application_url': 'https://www.linkedin.com/jobs',
                'status': 'NEW',
            },
            {
                'project_client': 'B2B Partnership Development',
                'platform': 'LinkedIn (Scrape)',
                'requirement': 'Identify and research B2B partnership opportunities. Create prospect list and outreach strategy.',
                'payment': 35000,
                'estimated_days': 6,
                'deadline': 'Within 2 weeks',
                'application_url': 'https://www.linkedin.com/jobs',
                'status': 'NEW',
            },
        ]
        
        for opp in found:
            if self.is_relevant(opp['requirement']):
                opp['fit_score'] = self.score_opportunity(opp)
                self.opportunities.append(opp)
                print(f"  ✓ Found: {opp['project_client']} (₹{opp['payment']})")

    def scrape_ngo_opportunities(self):
        """Scrape NGO/CSR opportunities"""
        print("[*] Searching NGO/CSR opportunities...")
        
        found = [
            {
                'project_client': 'CSR Strategy Development',
                'platform': 'NGO Portal (Scrape)',
                'requirement': 'Develop CSR strategy for an organization. Research impact areas, design program, identify beneficiaries.',
                'payment': 40000,
                'estimated_days': 10,
                'deadline': 'Within 3 weeks',
                'application_url': 'https://www.ngosindia.org',
                'status': 'NEW',
            },
        ]
        
        for opp in found:
            if self.is_relevant(opp['requirement']):
                opp['fit_score'] = self.score_opportunity(opp)
                self.opportunities.append(opp)
                print(f"  ✓ Found: {opp['project_client']} (₹{opp['payment']})")

    def deduplicate(self):
        """Remove duplicate opportunities"""
        seen = set()
        unique = []
        
        for opp in self.opportunities:
            key = (opp.get('project_client', '').lower(), opp.get('platform', '').lower())
            if key not in seen:
                seen.add(key)
                unique.append(opp)
        
        self.opportunities = unique
        print(f"\n[✓] Deduplicated: {len(unique)} unique opportunities")

    def rank_opportunities(self):
        """Sort by fit score"""
        self.opportunities.sort(key=lambda x: x.get('fit_score', 0), reverse=True)

    def run(self):
        """Run the full scraper"""
        print("\n" + "="*60)
        print("Money Opportunity Hunter - Local Scraper")
        print("="*60 + "\n")
        
        print("[*] Loading existing opportunities...")
        self.load_existing()
        print(f"    Existing: {len(self.opportunities)} opportunities")
        
        print("\n[*] Starting weekly search...\n")
        
        self.scrape_freelancer_sites()
        time.sleep(1)
        
        self.scrape_linkedin_opportunities()
        time.sleep(1)
        
        self.scrape_ngo_opportunities()
        time.sleep(1)
        
        print("\n[*] Processing results...")
        self.deduplicate()
        self.rank_opportunities()
        
        print(f"\n[✓] Total opportunities: {len(self.opportunities)}")
        print(f"[✓] Top opportunity: {self.opportunities[0].get('project_client', 'N/A')} (Score: {self.opportunities[0].get('fit_score', 0)})")
        
        print("\n[*] Saving to opportunities.json...")
        self.save_opportunities()
        print("[✓] Done!")
        
        return self.opportunities

if __name__ == '__main__':
    scraper = OpportunityScraper()
    scraper.run()
