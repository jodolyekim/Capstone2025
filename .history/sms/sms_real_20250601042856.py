import os
import uuid
import time
import datetime
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

def get_signature(secret_key, message):
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def send_sms_real(phone, text):
    api_key = os.getenv("COOLSMS_API_KEY")
    api_secret = os.getenv("COOLSMS_API_SECRET")
    sender = os.getenv("COOLSMS_SENDER_NUMBER")

    if not all([api_key, api_secret, sender]):
        raise Exception("쿨SMS API 키, 시크릿 또는 발신번호가 누락되었습니다.")

    # 인증 헤더 생성
    date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    salt = uuid.uuid4().hex
    signature = get_signature(api_secret, date + salt)

    headers = {
        "Authorization": f"HMAC-SHA256 ApiKey={api_key}, Date={date}, salt={salt}, signature={signature}",
        "Content-Type": "application/json; charset=utf-8"
    }

    data = {
        "messages": [
            {
                "to": phone,
                "from": sender,
                "text": text
            }
        ]
    }

    response = requests.post("https://api.coolsms.co.kr/messages/v4/send-many", headers=headers, json=data)

    if response.status_code == 200:
        print("✅ 문자 전송 성공:", response.json())
    else:
        print("❌ 문자 전송 실패:", response.status_code, response.text)
        raise Exception("문자 전송 실패")
