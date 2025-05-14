import re

# 욕설/민감 정보 정규표현식 (우회 표현 포함)
FILTER_PATTERNS = {
    "욕설": [
        r'ㅅㅂ|ㅆㅂ|씨발|시발|sibal|cibal|시ㅂ',
        r'ㅂㅅ|볍신|병ㅅ|byeongshin',
        r'ㄱㅅㄲ|개ㅅㅋ|개색기|gaesaekki',
        r'fuck|f[\W_]*u[\W_]*c[\W_]*k',
        r'bitch|b[\W_]*i[\W_]*t[\W_]*c[\W_]*h',
        r'asshole|a[\W_]*s[\W_]*s[\W_]*h[\W_]*o[\W_]*l[\W_]*e',
    ],
    "URL": [
        r'h[\W_]*t[\W_]*t[\W_]*p[s]?[\W_]*://',
        r'www[\W_]*\.', r'\S+\.com',
    ],
    "주민번호": [r'\d{6}[-\s]?\d{7}'],
    "이메일주소": [r'[a-zA-Z0-9_.+-]+\s*(\(at\)|\[at\]|@|＠|골뱅이)\s*[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'],
    "계좌번호": [r'\d{2,4}[-\s]?\d{3,6}[-\s]?\d{4,6}'],
    "카드번호": [r'\b(?:\d[ -]*?){13,16}\b'],
}

# 필터링 함수
def check_predefined_patterns(message: str) -> list:
    detected = []
    for category, patterns in FILTER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                detected.append(category)
                break
    return detected
