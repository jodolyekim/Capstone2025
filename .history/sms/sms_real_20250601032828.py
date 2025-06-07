import os
from dotenv import load_dotenv
from message import Message

load_dotenv()

def send_sms_real(phone, text):
    api_key = os.getenv("COOLSMS_API_KEY")
    api_secret = os.getenv("COOLSMS_API_SECRET")

    if not api_key or not api_secret:
        raise Exception("쿨SMS API 키 또는 시크릿이 누락되었습니다.")

    params = {
        'type': 'SMS',
        'to': phone,
        'from': '01012345678',  # 쿨SMS에 등록한 번호로 교체
        'text': text
    }

    cool = Message(api_key, api_secret)
    response = cool.send(params)

    if response.get('status') != "success":
        raise Exception(f"쿨SMS 전송 실패: {response}")
