import os
import requests
import feedparser
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_QUERIES = [
    # Korea
    '"Saudi Arabia" "South Korea" business',
    '"Saudi Arabia" "Korean company"',
    '"NEOM" "South Korea"',
    '"Aramco" "South Korea"',
    '"사우디" "한국 기업"',
    '"사우디" "수주"',
    '"사우디" "계약"',
    '"사우디" "진출"',

    # US / AI / Big Tech
    '"Saudi Arabia" "NVIDIA"',
    '"Saudi Arabia" "AMD"',
    '"Saudi Arabia" "Microsoft"',
    '"Saudi Arabia" "Google Cloud"',
    '"Saudi Arabia" "Oracle"',
    '"Saudi Arabia" "Amazon Web Services"',
    '"Saudi Arabia" "OpenAI"',
    '"Saudi Arabia" "data center"',
    '"Saudi Arabia" "AI chip"',

    # China
    '"Saudi Arabia" "Huawei"',
    '"Saudi Arabia" "Alibaba Cloud"',
    '"Saudi Arabia" "Tencent"',
    '"Saudi Arabia" "ZTE"',
    '"Saudi Arabia" "China" "AI"',
    '"Saudi Arabia" "China" "investment"',

    # Saudi institutions
    '"Aramco" "AI"',
    '"PIF" "technology"',
    '"NEOM" "data center"',
    '"HUMAIN" "NVIDIA"',
    '"HUMAIN" "AI"',
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

print("News sent")
