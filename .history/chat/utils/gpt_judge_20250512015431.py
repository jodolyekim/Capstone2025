import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'  # 실제 키로 교체

def is_sensitive_message(message: str) -> bool:
    """
    해당 메시지가 욕설/민감정보인지 GPT에게 물어보고 판단 결과를 bool로 반환
    """
    prompt = f"""다음 문장이 욕설이거나 민감한 개인정보(이메일, 계좌, 주소, 전화번호 등)에 해당하는지 판단해줘.
그렇다면 "YES", 아니라면 "NO"만 답해줘.

문장: "{message}"
답:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response.choices[0].message["content"].strip().upper()
        return answer == "YES"
    except Exception as e:
        print("GPT 판단 실패:", e)
        return True  # 예외 시 보수적으로 차단
