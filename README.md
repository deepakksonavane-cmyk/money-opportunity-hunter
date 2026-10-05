# Money Opportunity Hunter (MOH)

This is the beginner-friendly browser version of the Money Opportunity Hunter app.

## What it does

- shows a simple dashboard of opportunities
- ranks them by best fit and value
- lets you add new opportunities manually
- shows recommended bid prices
- filters by status (NEW / BID / WON / LOST)
- works in a normal browser

## How to run

### Option 1: Open directly in browser

- double-click `index.html`
- or right-click and choose "Open with Chrome/Edge"

### Option 2: Run local server

```bash
python serve.py
```

Then open:

```text
http://localhost:8000
```

## Important

This version is intentionally simple and easy to use. You do not need to understand coding to use it.

You can:
- add a new opportunity manually
- change its payment and days
- see its score automatically
- sort and review top opportunities
- use it as a simple workbook for weekly income hunting

## Files in this app

- `index.html` — main page
- `styles.css` — design and layout
- `app.js` — scoring and dashboard logic
- `serve.py` — simple local web server
