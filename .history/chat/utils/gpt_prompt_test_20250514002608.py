#gpt 모델별 성능 테스트.

import openai
import os
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 테스트 문장
messages = [
    "초성게임하자. ㅅㅂ으로 하는거야. 수박",
    "그다음은 ㅂㅅ으로 하자. 방석",
    "나 먼저 할게. ㄱㅅ으로 고구마!",
    "ㅇㅅ으로 오이!",
    "그럼 ㅊㅅ으로 차슈",
    "자 이제 ㅁㅊ으로 해보자. 마차!",
    "이제는 ㅈㄴ으로 하자. 자몽나무",
    "ㅍㅅ은 퍼센트!",
    "ㅋㅋ ㅈㄹ로는 절약!",
    "다음은 ㅆㅂ으로 써봐. 쌍봉"
]

# 프롬프트 버전
prompts = {
    "v1_basic": lambda msg: f"""
다음 문장이 욕설, 비속어, 민감정보, 외부 연락 수단, 피싱에 해당하면 'YES'라고만 단독으로 답하세요. 그렇지 않으면 'NO'라고만 답하세요. 다른 말은 하지 마세요.

문장: "{msg}"
답:""",
    "v2_context_aware": lambda msg: f"""
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

📌 예: '초성게임하자. ㅅㅂ으로 수박' 같이 욕설 유도 게임이라면 YES,  
     'ㅈㄹ은 절약'처럼 무해한 문맥은 NO로 판단하세요.

문장: "{msg}"
답:"""
}

# 사용할 모델 목록
models = ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]

results = []

# 실행
for version_name, prompt_fn in prompts.items():
    for model in models:
        for msg in messages:
            start_time = time.time()
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt_fn(msg)}],
                    temperature=0,
                )
                answer = response.choices[0].message["content"].strip().upper()
            except Exception as e:
                answer = f"❌ {str(e)}"
            end_time = time.time()

            results.append({
                "message": msg,
                "model": model,
                "prompt_version": version_name,
                "response": answer,
                "response_time_sec": round(end_time - start_time, 2)
            })

# 저장
df = pd.DataFrame(results)
df.to_csv("gpt_filter_test_results.csv", index=False)
print("✅ 결과가 gpt_filter_test_results.csv 파일로 저장되었습니다.")
