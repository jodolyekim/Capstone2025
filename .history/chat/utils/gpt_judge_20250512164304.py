# chat/utils/gpt_judge.py

import sys
import os
import openai
from dotenv import load_dotenv

# 디버깅용: 현재 Python 실행 환경 및 경로 출력
print("🐍 실행 Python:", sys.executable)
print("📦 설치 경로 목록:")
for path in sys.path:
    print("   -", path)

# .env 파일에서 API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_sensitive_message(message: str) -> bool:
    """
    GPT-4-1-Nano 모델을 이용해 메시지가 민감한 내용인지 판단
    욕설, 개인정보, 연락처, SNS 공유 등 포함 여부를 검사
    민감한 경우 True 반환 (전송 차단), 문제 없으면 False 반환 (전송 허용)
    """
    prompt = f"""다음 문장이 욕설이거나 민감한 개인정보(이메일, 계좌, 주소, 전화번호 등)에 해당하는지 판단해줘.
그렇다면 "YES", 아니라면 "NO"만 답해줘.

문장: "{message}"
답:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1-nano",  # ✅ 너가 사용할 수 있는 Nano 모델명
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message["content"].strip().upper()
        return answer == "YES"
    except Exception as e:
        print("❌ GPT 판단 실패:", e)
        return True  # 예외 시 안전하게 차단
