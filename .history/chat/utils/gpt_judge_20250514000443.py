import sys
import os
import openai
from dotenv import load_dotenv

# .env에서 OPENAI_API_KEY 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
print("🔐 API 키 확인:", api_key[:10] if api_key else "없음")  # 앞 10자리만 출력

def is_sensitive_message(message: str) -> bool:
    """
    문맥 기반 욕설/비속어/민감정보/피싱 가능성 판단용 GPT 호출 (모델: gpt-4o-mini)
    'YES'만 정확히 일치할 때만 차단. 그 외는 전송 허용
    """
    prompt = f"""
아래 문장을 읽고, 문장이 실제로 욕설, 비속어, 민감정보, 피싱 의도가 포함된 **문맥적 위험 문장인지** 판단하세요.

⚠️ 다음 중 하나라도 포함되면 'YES'라고만 단독으로 답하세요:
1. 욕설 또는 비속어 (예: 씨발, 병신, fuck 등)
2. 개인정보 제공 의도 (전화번호, 주소, 계좌번호, 주민번호, 이메일 등 실제 정보 전달 시도)
3. 외부 연락처 공유 (SNS 아이디, 카카오톡, 디스코드, 텔레그램 등)
4. 피싱이나 사기 목적 문장 또는 URL

⚠️ 하지만 아래와 같은 경우는 'NO'로 답하세요:
- 사용자가 민감 정보를 주지 않겠다고 거절하는 경우
- 민감 단어가 등장하지만 실제로는 보호 의도, 경고, 농담인 경우
- 정보 전달 없이 단어만 언급되거나 문맥상 안전한 경우

📝 주의사항:
- 반드시 'YES' 또는 'NO' 중 하나만 단독으로 출력하세요.
- 설명, 따옴표, 이유 등은 쓰지 마세요. 오직 YES 또는 NO만 출력해야 합니다.

문장: "{message}"
답:"""

    try:
        print("📤 GPT 판단 요청:", message)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message["content"].strip().upper()
        print("🧠 GPT 응답:", answer)

        if answer == "YES":
            return True
        elif answer == "NO":
            return False
        else:
            print("⚠️ GPT 응답이 이상함:", answer)
            return False
    except Exception as e:
        print("❌ GPT 판단 실패:", e)
        return False
