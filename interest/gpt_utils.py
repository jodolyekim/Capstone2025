import os
import openai
import json
import re
from dotenv import load_dotenv

# 🔐 .env 환경변수에서 API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_keywords_by_gpt(text):
    prompt = f"""
너는 사용자의 자기소개 문장에서 관심 키워드를 뽑아주는 AI야.

다음 문장에서 관심 키워드를 3~10개 정도 뽑고, 너무 구체적인 표현은 하나의 일반적인 키워드로 묶어줘.
예를 들어:
- "축구 보기", "축구 직관", "축구 하는 것" → "축구"
- "공원 산책", "산책하기", "자연 걷기" → "산책"
- "요리 배우기", "요리 프로그램 보기" → "요리"

반드시 중복된 키워드 없이, 가능한 한 넓고 일반적인 표현으로 추출해.
그리고 키워드는 카테고리별로 나눠서 JSON 형식만 반환해줘.
설명은 절대 하지 마.

예시:
{{
  "취미": ["산책", "요리"],
  "스포츠": ["축구"],
  "동물": ["강아지"]
}}

자기소개: "{text}"
"""


    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        content = response.choices[0].message["content"].strip()
        print("[GPT 응답 내용]:", content)

        # ✅ ```json 또는 ``` 제거
        content = re.sub(r"^```json\s*|```$", "", content, flags=re.IGNORECASE).strip()

        # ✅ JSON 파싱
        result = json.loads(content)

        if not isinstance(result, dict):
            raise ValueError("GPT 응답이 올바른 JSON 객체 형식이 아닙니다.")

        return result

    except json.JSONDecodeError as je:
        print(f"[JSON 파싱 오류]: {je}")
        print("[응답 원문]:", content)
        return {}
    except Exception as e:
        print(f"[OpenAI 오류]: {e}")
        return {}
