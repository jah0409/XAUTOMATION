# Free AI Twitter/X Automation Bot (Python)

This project is a beginner-friendly, low-cost automation bot that:
- pulls trending AI topics from **Reddit + Google News RSS**,
- generates human-like curiosity-driven tweets with **Groq API**,
- posts to X/Twitter via **Playwright web automation**,
- runs automatically **5 times daily**,
- avoids duplicate tweets and stores history locally.

## Project Structure

```bash
.
├── .env.example
├── .github/
│   └── workflows/
│       └── bot.yml
├── requirements.txt
├── README.md
└── src/
    ├── main.py
    └── bot/
        ├── config.py
        ├── generator.py
        ├── logger.py
        ├── scheduler.py
        ├── storage.py
        ├── trends.py
        └── twitter_client.py
```

## 1) Setup Step-by-Step

### A. Clone and create virtual environment
```bash
git clone <your-repo-url>
cd XAUTOMATION
python -m venv .venv
source .venv/bin/activate
```

### B. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### C. Configure secrets
```bash
cp .env.example .env
```
Fill all values in `.env`.

### D. Run one test post
```bash
python src/main.py --once
```

### E. Run scheduler (5x daily)
```bash
python src/main.py
```
Default UTC schedule: `08:00,11:00,14:00,17:00,20:00`.

## 2) How It Works

1. `trends.py` fetches hot AI titles from Reddit and Google News RSS.
2. `generator.py` asks Groq to write one human-sounding tweet under 240 chars.
3. `storage.py` checks history to avoid duplicates.
4. `twitter_client.py` uses Playwright to log in and post with:
   - human typing simulation,
   - random delays.
5. `scheduler.py` runs this flow 5 times per day.

## 3) GitHub Actions (Free Automation)

The included workflow runs on a cron schedule and posts once per run.

### Add these GitHub Secrets
- `GROQ_API_KEY`
- `GROQ_MODEL`
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`
- `X_EMAIL`
- `X_USERNAME`
- `X_PASSWORD`

### Workflow behavior
- installs Python deps,
- installs Playwright Chromium,
- ensures a local tweet history file exists in the workspace,
- runs `python src/main.py --once`.

## 4) Keep It Running 24/7

### Option A (Recommended): GitHub Actions
- Free, serverless scheduling.
- Great for lightweight bot automation.

### Option B: VPS + systemd
- More reliable browser automation.
- Full control over long-running processes.

## Notes

- X may trigger extra verification challenges in automated login flows.
- For stable long-term use, prefer session/cookie persistence and anti-lock safeguards.
- Keep content compliant with X policies.
