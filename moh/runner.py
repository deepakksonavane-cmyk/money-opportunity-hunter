from .sources import search_opportunities
from .filters import filter_opportunities
from .scorer import rank_opportunities
from .dashboard import export_csv, print_dashboard


def run(source_urls=None, json_path=None, top_n=10):
    raw = search_opportunities(source_urls=source_urls, json_path=json_path)
    eligible = filter_opportunities(raw)
    ranked = rank_opportunities(eligible)
    print_dashboard(ranked, top_n=top_n)
    export_csv(ranked, "moh_dashboard.csv")
    print("Saved: moh_dashboard.csv")
    return ranked


if __name__ == "__main__":
    run()
