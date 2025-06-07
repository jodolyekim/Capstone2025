import os
from dotenv import load_dotenv
from coolsms import Message

load_dotenv()

def send_sms_real(phone, text):
    api_key = os.getenv("COOLSMS_API_KEY")
    api_secret = os.getenv("COOLSMS_API_SECRET")

    if not api_key or not api_secret:
        raise Exception("쿨SMS API 키 또는 시크릿이 .env에서 누락되었습니다.")

    message = Message(api_key, api_secret)

    params = {
        'to': phone,
        'from': '발신번호',  # 쿨SMS에 등록된 번호로 교체
        'text': text,
        'type': 'SMS',
    }

    response = message.send(params)
    
    if response.get('status') != "success":
        raise Exception(f"쿨SMS 문자 전송 실패: {response}")
