import os
import requests
import feedparser
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_QUERIES = [
    "Saudi Arabia business",
    "Saudi Arabia investment",
    "Saudi Arabia contract",
    "Saudi Arabia project",
    "Saudi Arabia AI",
    "Saudi Arabia data center",
    "Saudi Arabia NVIDIA",
    "Saudi Arabia AMD",
    "Saudi Arabia Microsoft",
    "Saudi Arabia Google",
    "Saudi Arabia Oracle",
    "Saudi Arabia Huawei",
    "Saudi Arabia China",
    "Saudi Arabia South Korea",
    "NEOM project",
    "NEOM investment",
    "Aramco technology",
    "PIF investment",
    "HUMAIN AI",
    "사우디 투자",
    "사우디 계약",
    "사우디 수주",
    "사우디 AI",
    "사우디 데이터센터",
    "네옴 프로젝트",
    "아람코 투자",
    "PIF 투자",
]

EXCLUDE_KEYWORDS = [
    "football", "soccer", "transfer", "tourism", "travel",
    "oil price", "crude oil", "war", "israel", "iran",
    "축구", "이적", "관광", "여행", "유가", "전쟁"
]

articles = []

for query in SEARCH_QUERIES:
    rss_url = (
        "https://news.google.com/rss/search?q="
        + requests.utils.quote(query)
        + "&hl=ko&gl=KR&ceid=KR:ko"
    )

    feed = feedparser.parse(rss_url)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        source = entry.get("source", {}).get("title", "")

        title_lower = title.lower()

        if any(word.lower() in title_lower for word in EXCLUDE_KEYWORDS):
            continue

        articles.append({
            "title": title,
            "source": source,
            "link": link
        })

seen = set()
unique_articles = []

for article in articles:
    if article["title"] not in seen:
        seen.add(article["title"])
        unique_articles.append(article)

unique_articles = unique_articles[:20]

today = datetime.now().strftime("%Y-%m-%d")

message = f"📌 Saudi Business Intelligence ({today})\n"
message += "한국·미국·중국·엔비디아 사우디 동향\n\n"

if not unique_articles:
    message += "관련 신규 기사를 찾지 못했습니다."
else:
    for idx, article in enumerate(unique_articles, start=1):
        message += (
            f"{idx}. {article['title']}\n"
            f"- {article['source']}\n"
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

print(f"Articles found: {len(unique_articles)}")
print("News sent")
