import os
import requests
import feedparser
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_QUERIES = [

```
# 사우디 핵심
"사우디",
"사우디아라비아",
"네옴",
"아람코",
"PIF",

# 한국 기업 동향
"사우디 한국기업",
"사우디 수주",
"사우디 계약",
"사우디 협약",
"사우디 투자",
"사우디 진출",
"사우디 사업 확대",
"사우디 데이터센터",
"사우디 AI",
"사우디 디지털트윈",

# 실제 기사 대응
"리벨리온 사우디",
"네이버 사우디",
"LX공사 사우디",
"삼성E&A 사우디",
"현대건설 사우디",
"포스코 사우디",
"두산에너빌리티 사우디",

# 영어권
"Saudi Arabia",
"Saudi Arabia investment",
"Saudi Arabia contract",
"Saudi Arabia project",
"Saudi Arabia AI",
"Saudi Arabia data center",

"Saudi Arabia South Korea",
"Saudi Arabia Korean company",

"NEOM",
"Aramco",
"PIF",

# 미국
"Saudi Arabia NVIDIA",
"Saudi Arabia AMD",
"Saudi Arabia Microsoft",
"Saudi Arabia Google",
"Saudi Arabia Oracle",
"Saudi Arabia OpenAI",

# 중국
"Saudi Arabia Huawei",
"Saudi Arabia Alibaba",
"Saudi Arabia Tencent"
```

]

EXCLUDE_KEYWORDS = [
"축구",
"이적",
"관광",
"여행",
"유가",
"전쟁",
"football",
"soccer",
"transfer",
"tourism",
"travel",
"oil price"
]

articles = []

for query in SEARCH_QUERIES:

```
rss_url = (
    "https://news.google.com/rss/search?q="
    + requests.utils.quote(query)
    + "&hl=ko&gl=KR&ceid=KR:ko"
)

try:
    feed = feedparser.parse(rss_url)

    for entry in feed.entries:

        title = entry.title
        link = entry.link
        source = entry.get("source", {}).get("title", "")

        title_lower = title.lower()

        if any(
            keyword.lower() in title_lower
            for keyword in EXCLUDE_KEYWORDS
        ):
            continue

        articles.append({
            "title": title,
            "source": source,
            "link": link
        })

except Exception:
    pass
```

seen = set()
unique_articles = []

for article in articles:

```
if article["title"] not in seen:
    seen.add(article["title"])
    unique_articles.append(article)
```

unique_articles = unique_articles[:20]

today = datetime.now().strftime("%Y-%m-%d")

message = f"📌 Saudi Business Intelligence ({today})\n"
message += "사우디 · 한국 · 미국 · 중국 기업 동향\n\n"

if not unique_articles:
message += "관련 신규 기사를 찾지 못했습니다."

else:

```
for idx, article in enumerate(unique_articles, start=1):

    message += (
        f"{idx}. {article['title']}\n"
        f"- {article['source']}\n"
        f"{article['link']}\n\n"
    )
```

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
