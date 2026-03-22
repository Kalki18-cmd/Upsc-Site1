# fetch_news.py
# Generates news.json from PIB RSS for a static site (no Firebase).
# Run locally: python fetch_news.py
# GitHub Actions will run this daily at 06:00 IST.

import json
import re
import hashlib
from datetime import datetime, timezone
from typing import List, Dict
import feedparser

FEEDS = [
    {"name": "PIB", "url": "https://pib.gov.in/rss.aspx"},
]

CATEGORY_KEYWORDS = {
    "Polity": [
        "constitution", "article ", "parliament", "loksabha", "rajyasabha", "judiciary",
        "supreme court", "high court", "bill", " act ", "amendment", "governor",
        "president", "election commission",
    ],
    "Economy": [
        "budget", "gdp", "inflation", "cpi", "wpi", "rbi", "monetary policy", "fiscal",
        "tax", "gst", "msme", "fdi", "exports", "imports", "current account", "bank",
    ],
    "Environment": [
        "climate", "pollution", "wildlife", "forest", "biodiversity", "emissions",
        "carbon", "environment", "conservation", "ecology", "sustainable", "cop",
    ],
    "International Relations": [
        "foreign minister", "bilateral", "summit", "treaty", "quad", "unsc", "diplomatic",
        "embassy", "india-japan", "india-us", "india-france", "visit", "strategic",
    ],
}

MAX_ITEMS = 40  # limit for a lightweight page

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)  # strip HTML
    s = re.sub(r"\s+", " ", s).strip()
    return s

def categorize(title: str, summary: str):
    text = (title + " " + summary).lower()
    matched = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if re.search(rf"(?<!\w){re.escape(kw)}(?!\w)", text):
                matched.append(cat)
                break
    return matched or ["General"]

def make_id(link: str, title: str) -> str:
    base = (link or "") + "|" + (title or "")
    return hashlib.sha256(base.encode()).hexdigest()[:16]

def fetch() -> List[Dict]:
    items: List[Dict] = []
    for f in FEEDS:
        parsed = feedparser.parse(f["url"])
        for e in parsed.entries:
            title = clean_text(getattr(e, "title", ""))
            if not title:
                continue
            summary = clean_text(getattr(e, "summary", ""))
            link = getattr(e, "link", "")
            pub = getattr(e, "published", "") or getattr(e, "updated", "")
            cats = categorize(title, summary)
            items.append({
                "id": make_id(link, title),
                "title": title,
                "summary": summary,
                "link": link,
                "published": pub,
                "source": f["name"],
                "categories": cats
            })
    # Deduplicate and trim
    seen = {}
    for it in items:
        seen[it["id"]] = it
    out = list(seen.values())
    # Sort newest first if date is present
    def sort_key(x):
        return x.get("published", "")
    out.sort(key=sort_key, reverse=True)
    return out[:MAX_ITEMS]

def main():
    items = fetch()
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} items to news.json at", datetime.now(timezone.utc).isoformat())

if __name__ == "__main__":
    main()
