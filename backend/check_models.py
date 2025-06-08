import openai
from dotenv import load_dotenv
import os

# .env에서 API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 모델 목록 출력
response = openai.Model.list()

print("🧠 사용 가능한 모델 목록:")
for model in response['data']:
    print("-", model['id'])
