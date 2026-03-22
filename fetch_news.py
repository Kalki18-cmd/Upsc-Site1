import os, re, json, hashlib, feedparser, requests
from datetime import datetime, timezone, timedelta

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"   # adjustable
RSS = "https://pib.gov.in/rss.aspx"

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()

def prompt(title, summary):
    return f"""
Generate UPSC exam oriented notes in JSON with keys:
why_in_news, key_facts, prelims_pointers, mains_angle, gs_paper, topic, tags.
Make it crisp and factual.

Title: {title}
Summary: {summary}
"""

def ask_ai(p):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_KEY}"},
        json={
            "model": MODEL,
            "messages":[
                {"role":"system","content":"UPSC mentor. Respond only in JSON."},
                {"role":"user","content":p}
            ],
            "response_format":{"type":"json_object"},
            "temperature":0.2
        }
    )
    return json.loads(r.json()["choices"][0]["message"]["content"])

def main():
    feed = feedparser.parse(RSS)
    out = []
    for e in feed.entries[:20]:
        title = clean(e.title)
        summary = clean(e.summary)
        link = e.link
        pub = e.published if hasattr(e,"published") else ""

        ai = ask_ai(prompt(title, summary))

        out.append({
            "id": hashlib.md5((title+link).encode()).hexdigest(),
            "title": title,
            "source": "PIB",
            "published": pub,
            "summary": {
                "why_in_news": ai.get("why_in_news",""),
                "key_facts": ai.get("key_facts",""),
                "prelims_pointers": ai.get("prelims_pointers",""),
                "mains_angle": ai.get("mains_angle",""),
            },
            "gs_paper": ai.get("gs_paper",""),
            "topic": ai.get("topic",""),
            "tags": ai.get("tags",[])
        })

    with open("ai_news.json","w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=2)

if __name__ == "__main__":
    main()
