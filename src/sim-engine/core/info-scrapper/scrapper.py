import requests
import time
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # <<< PUT YOUR KEY HERE
OUTPUT_FILE = "news_data.jsonl"

LANGUAGE = "vi"
PAGE_SIZE = 100
FROM_DATE = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
QUERIES = [
    "bóng đá",
    "chính trị",
    "giải trí",
    "kinh tế",
    "giáo dục",
    "thời tiết",
    "pháp luật",
    "sức khỏe",
]

OUTPUT_FILE = "articles.json"


def fetch_articles(query, page):
    print(f"📄 Fetching '{query}' | page {page}...")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": LANGUAGE,
        "from": FROM_DATE,
        "pageSize": PAGE_SIZE,
        "page": page,
        "apiKey": NEWS_API_KEY,
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"❌ Error {resp.status_code}: {resp.text}")
        return []
    return resp.json().get("articles", [])


def save_articles(all_articles, base_filename="articles"):
    i = 1
    while True:
        filename = f"{base_filename}_{i}.json"
        if not os.path.exists(filename):
            break
        i += 1

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to {filename}. Total articles: {len(all_articles)}")


def main():
    print("🚀 Starting NewsAPI crawl with query rotation...")
    all_articles = []
    for query in QUERIES:
        articles = fetch_articles(query, 1)
        all_articles.extend(articles)
        time.sleep(1)
    save_articles(all_articles)


if __name__ == "__main__":
    main()
