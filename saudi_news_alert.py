import os
import requests
import feedparser
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_QUERIES = [
    "Saudi Arabia Korea company",
    "Saudi Arabia Korean company contract",
    "Saudi Arabia Korean company MOU",
    "NEOM Korean company",
    "Aramco Korean company",
    "PIF Korean company",
    "사우디 한국기업",
    "사우디 수주",
    "사우디 계약",
    "네옴 한국기업"
]

KOREAN_COMPANIES = [
    "삼성", "현대", "포스코", "한화", "LG", "SK",
    "두산", "네이버", "KT", "리벨리온",
    "Samsung", "Hyundai", "POSCO", "Hanwha",
    "LG", "SK", "Naver", "Rebellions"
]

articles = []

for query in SEARCH_QUERIES:
    rss_url = f"https://news.google.com/rss/search?q={query}"

    try:
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            if any(company.lower() in title.lower() for company in KOREAN_COMPANIES):
                articles.append({
                    "title": title,
                    "link": link
                })

    except Exception:
        pass

# 중복 제거
seen = set()
unique_articles = []

for article in articles:
    if article["title"] not in seen:
        seen.add(article["title"])
        unique_articles.append(article)

# 최대 20건
unique_articles = unique_articles[:20]

today = datetime.now().strftime("%Y-%m-%d")

message = f"📌 사우디 한국기업 동향 ({today})\n\n"

if not unique_articles:
    message += "관련 신규 기사를 찾지 못했습니다."
else:
    for idx, article in enumerate(unique_articles, start=1):
        message += (
            f"{idx}. {article['title']}\n"
            f"{article['link']}\n\n"
        )

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("News sent")
