import os
import requests
import feedparser
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_QUERIES = [
"Saudi Arabia Korea contract",
"Saudi Arabia Korea investment",
"Saudi Arabia Korea MOU",
"Saudi Arabia Korea project",
"Saudi Arabia Korean company",
"NEOM Korea",
"Aramco Korea",
"PIF Korea",
"사우디 수주",
"사우디 계약",
"사우디 투자",
"사우디 진출",
"네옴 프로젝트",
"아람코 한국기업"
]

BUSINESS_KEYWORDS = [
"contract", "project", "investment", "mou",
"agreement", "deal", "partnership",
"수주", "계약", "투자", "협약",
"진출", "합작", "공급", "사업"
]

articles = []

for query in SEARCH_QUERIES:

```
rss_url = (
    "https://news.google.com/rss/search?q="
    + requests.utils.quote(query)
)

try:
    feed = feedparser.parse(rss_url)

    for entry in feed.entries:

        title = entry.title
        link = entry.link

        title_lower = title.lower()

        if any(
            keyword.lower() in title_lower
            for keyword in BUSINESS_KEYWORDS
        ):
            articles.append({
                "title": title,
                "link": link
            })

except Exception:
    pass
```

seen = set()
unique_articles = []

for article in articles:
if article["title"] not in seen:
seen.add(article["title"])
unique_articles.append(article)

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
