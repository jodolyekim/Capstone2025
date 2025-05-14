# chat/utils/gpt_judge.py

import sys
import os
import openai
from dotenv import load_dotenv

# .env에서 OPENAI_API_KEY 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_sensitive_message(message: str) -> bool:
    """
    민감 정보/욕설 판단용 GPT 호출 (모델: gpt-4-1-nano)
    'YES'만 정확히 일치할 때만 차단. 나머지는 전송 허용
    """
    prompt = f"""
다음 문장이 욕설, 비속어, 개인정보(이메일, 전화번호, 주소, 계좌, SNS 아이디 등), 혹은 외부 연락 수단을 포함하면 "YES"라고만 단독으로 답하세요.
그렇지 않으면 "NO"라고만 단독으로 답하세요.
다른 말은 절대 하지 마세요. 반드시 YES 또는 NO 중 하나만 단독으로 출력하세요.

문장: "{message}"
답:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1-nano",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message["content"].strip().upper()

        # ✅ 'YES'만 정확히 일치해야 차단됨
        if answer == "YES":
            return True  # 차단
        elif answer == "NO":
            return False  # 통과
        else:
            print("⚠️ GPT 응답이 이상함:", answer)
            return False  # 이상한 응답은 통과 처리
    except Exception as e:
        print("❌ GPT 판단 실패:", e)
        return False  # 예외도 통과로 처리 (너무 보수적이면 문제)
