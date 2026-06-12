import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = """
📌 Saudi Business Intelligence

테스트 성공!

앞으로 이 봇이
사우디·네옴·아람코·PIF·한국기업·엔비디아 관련 뉴스를 보내게 됩니다.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Saudi Business Bot OK")
