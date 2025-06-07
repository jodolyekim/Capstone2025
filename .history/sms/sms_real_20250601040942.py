import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_sms_real(phone, text):
    api_key = os.getenv("COOLSMS_API_KEY")
    api_secret = os.getenv("COOLSMS_API_SECRET")
    sender = os.getenv("COOLSMS_SENDER", "01012345678")

    if not api_key or not api_secret:
        raise Exception("쿨SMS API 키 또는 시크릿이 .env에 설정되어 있지 않습니다.")

    url = "https://api.coolsms.co.kr/messages/v4/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"HMAC {api_key}:{api_secret}",
    }

    payload = {
        "messages": [
            {
                "to": phone,
                "from": sender,
                "text": text,
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"쿨SMS 전송 실패: {response.text}")

    result = response.json()
    if result.get('statusCode') != "2000":
        raise Exception(f"쿨SMS 응답 오류: {result}")
