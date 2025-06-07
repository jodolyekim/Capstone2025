import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_sms_real(phone, text):
    api_key = os.getenv("COOLSMS_API_KEY")
    api_secret = os.getenv("COOLSMS_API_SECRET")
    sender = os.getenv("COOLSMS_SENDER", "01012345678")  # 쿨SMS에 등록한 발신번호

    if not api_key or not api_secret:
        raise Exception("쿨SMS API 키 또는 시크릿이 .env에 설정되어 있지 않습니다.")

    url = "https://api.coolsms.co.kr/sms/2/send"  # ✅ v2 API 사용

    payload = {
        'key': api_key,
        'secret': api_secret,
        'to': phone,
        'from': sender,
        'text': text,
        'type': 'sms'
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"쿨SMS 전송 실패: {response.text}")

    result = response.json()
    if result.get('result_code') != '1':
        raise Exception(f"쿨SMS 응답 오류: {result}")
