# Money Opportunity Hunter (MOH)

A lightweight autonomous agent for finding small, legitimate, paid opportunities worldwide that match Deepak Sonavane's practical business and research capabilities.

## Objective

Find projects that can realistically be completed in 1–15 working days, pay ₹10,000–₹1,00,000+ (or equivalent), and require business thinking, market research, commercial analysis, customer discovery, vendor research, feasibility studies, territory mapping, project planning, documentation, or implementation planning.

## Principles

- Search first, then filter, then score
- Prioritize quick-win work over long-term noise
- Reject low-value and scam-like jobs
- Rank the best 10 first
- Keep the system modular and easy to extend

## MVP workflow

1. Search available opportunities
2. Normalize/extract them
3. Reject junk, scams, and generic work
4. Score with fit/pay/time/credibility/win probability
5. Present a ranked dashboard

## Folder structure

```text
moh/
  __init__.py
  models.py
  sources.py
  filters.py
  scorer.py
  dashboard.py
  runner.py
requirements.txt
README.md
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m moh.runner
```

## Output

- Terminal dashboard showing the best opportunities first
- CSV export: `moh_dashboard.csv`

## Notes

This is intentionally lightweight and easy to extend with new sources later. The first version focuses on a minimal but useful pipeline: search → extract → filter → score → dashboard.
