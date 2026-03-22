import os, json, re, hashlib, requests, feedparser

HUGGINGFACE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
TOKEN = os.getenv("HUGGINGFACE_TOKEN")
SITE_DIR = os.getenv("SITE_DIR", ".")
OUT_PATH = os.path.join(SITE_DIR, "ai_news.json")

FEED = "https://pib.gov.in/rss.aspx"
MAX_ITEMS = 20

def clean(s):
    if not s: return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def stable_id(link, title):
    return hashlib.sha1((link + title).encode()).hexdigest()[:12]

def call_hf(prompt):
    r = requests.post(
        f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"inputs": prompt, "parameters": {"max_new_tokens": 400}}
    )
    r.raise_for_status()
    txt = r.json()[0]["generated_text"]
    # try to extract json
    m = re.search(r"\{.*\}", txt, re.S)
    if not m: raise ValueError("No JSON in HF output")
    return json.loads(m.group(0))

def main():
    feed = feedparser.parse(FEED)
    out = []

    for e in feed.entries[:MAX_ITEMS]:
        title = clean(e.title)
        summary = clean(e.summary)
        link = e.link

        prompt = f"""
Write UPSC-ready JSON with keys:
why_in_news, key_facts, prelims_pointers, mains_angle, tags

News:
TITLE: {title}
SUMMARY: {summary}
        """

        try:
            ai = call_hf(prompt)
        except Exception as ex:
            ai = {
                "why_in_news": summary,
                "key_facts": "",
                "prelims_pointers": "",
                "mains_angle": "",
                "tags": []
            }

        out.append({
            "id": stable_id(link, title),
            "title": title,
            "source": "PIB",
            "categories": ["General"],
            "tags": ai.get("tags", []),
            "summary": {
                "why_in_news": ai.get("why_in_news", ""),
                "key_facts": ai.get("key_facts", ""),
                "prelims_pointers": ai.get("prelims_pointers", ""),
                "mains_angle": ai.get("mains_angle", "")
            }
        })

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
``
