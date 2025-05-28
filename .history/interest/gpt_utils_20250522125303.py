# interest/gpt_utils.py

import os
import openai
from dotenv import load_dotenv

# .env 파일 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_keywords_by_gpt(text):
    prompt = f"""다음 자기소개 문장에서 관심 키워드를 5~10개 추출해줘. 각 키워드를 카테고리별로 구분해서 JSON 형식으로 반환해줘.

예시 응답 형식:
{{
  "취미": ["산책", "요리"],
  "스포츠": ["탁구"],
  "동물": ["강아지"]
}}

자기소개: "{text}"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"[OpenAI 오류] {e}")
        return ""
