# Money Opportunity Hunter - Local Web Scraper

This is a **local web scraper** that runs weekly and finds real paid opportunities from the internet.

## What it does

1. Searches real job websites (Upwork, Fiverr, LinkedIn, etc.)
2. Finds opportunities that match your skills
3. Ranks them by best fit
4. Shows the top 10 in a simple dashboard
5. Saves everything locally

## How to use

### Step 1: Install Python (one-time setup)

- Download Python from: https://www.python.org/downloads/
- Install it
- Make sure to check "Add Python to PATH"

### Step 2: Download this project

- Go to: https://github.com/deepakksonavane-cmyk/money-opportunity-hunter
- Click Code → Download ZIP
- Unzip it
- Open the folder

### Step 3: Run the scraper

**On Windows:**
- Right-click inside the folder
- Choose "Open PowerShell here"
- Type: `python run_weekly.py`
- Press Enter

**On Mac/Linux:**
- Open Terminal
- Go to the folder: `cd money-opportunity-hunter`
- Type: `python run_weekly.py`
- Press Enter

### Step 4: Open the dashboard

- The scraper will run and collect opportunities
- Then automatically open a webpage in your browser
- You'll see all the opportunities ranked by best fit

## What you'll see

- **Top section**: Summary stats (total opportunities, average fit score, total payment value)
- **Filter buttons**: Click to see NEW / BID / WON / LOST opportunities
- **Opportunity list**: Each shows:
  - Project name and platform
  - What it's about
  - How much it pays
  - How many days it takes
  - A fit score (0-100)
  - Status badge

## How to add your own opportunities

After the scraper runs:
- Click **+ ADD NEW OPPORTUNITY**
- Fill in the details
- Click Save
- It saves automatically

## Run it weekly

Every week:
1. Open PowerShell/Terminal in the folder
2. Type: `python run_weekly.py`
3. Wait for it to finish
4. Review the opportunities in your browser

## Data

All data is saved locally on your computer in a file called `opportunities.json`. It never goes to anyone else.

## Troubleshooting

**"Python not found"**
- Make sure Python is installed
- Restart your computer after installing

**"No opportunities found"**
- This sometimes happens if websites block the scraper
- Run again tomorrow
- Or add your own opportunities manually

**Slow to load**
- First run takes longer (5-10 minutes)
- Next runs are faster

---

That's it! Run it weekly to keep your opportunity list fresh.
