import os
import openai
import json
from dotenv import load_dotenv

# .env 파일 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_keywords_by_gpt(text):
    prompt = f"""
너는 사용자의 자기소개 문장에서 관심 키워드를 뽑아주는 AI야.
다음 문장에서 관심 키워드를 3~10개 정도 뽑고, 카테고리별로 나눠서 아래 예시처럼 **JSON 형식만 반환해줘**.
설명은 절대 하지 마.

예시:
{{
  "취미": ["산책", "요리"],
  "스포츠": ["탁구"],
  "동물": ["강아지"]
}}

자기소개: "{text}"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 또는 gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message["content"].strip()

        print("[GPT 응답 내용]:", content)

        # JSON 파싱 시도
        result = json.loads(content)
        return result  # ✅ 바로 dict 반환

    except json.JSONDecodeError as je:
        print(f"[JSON 파싱 오류]: {je}")
        print("[응답 원문]:", content)
        return {}
    except Exception as e:
        print(f"[OpenAI 오류]: {e}")
        return {}
