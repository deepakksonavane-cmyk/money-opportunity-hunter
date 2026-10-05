import os
import json
import webbrowser
from scraper import OpportunityScraper
import time

def run_scraper():
    """Run the scraper and update opportunities"""
    print("\n[*] Fetching latest opportunities...\n")
    scraper = OpportunityScraper()
    opportunities = scraper.run()
    print("\n[✓] Scraping complete!")
    return opportunities

def open_dashboard():
    """Open the dashboard in browser"""
    dashboard_path = os.path.abspath('index.html')
    file_url = f'file:///{dashboard_path}'
    
    print(f"\n[*] Opening dashboard...")
    print(f"    {file_url}")
    
    time.sleep(2)
    webbrowser.open(file_url)
    print("\n[✓] Dashboard opened in browser!")
    print("\nYou can now:")
    print("  - See the top opportunities ranked by fit")
    print("  - Filter by status (NEW / BID / WON / LOST)")
    print("  - Add your own opportunities manually")
    print("  - Data is saved locally on your computer")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MONEY OPPORTUNITY HUNTER - WEEKLY RUN")
    print("="*60)
    
    # Step 1: Run scraper
    opportunities = run_scraper()
    
    # Step 2: Open dashboard
    open_dashboard()
    
    print("\n" + "="*60)
    print("Run again next week: python run_weekly.py")
    print("="*60 + "\n")
