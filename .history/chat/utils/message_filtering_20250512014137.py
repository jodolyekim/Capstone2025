import re

# 필터 패턴 정의 (욕설, 주민번호, 이메일, 주소, 카드번호, 등등)
FILTER_PATTERNS = {
    "욕설": [
        r'ㅅㅂ|ㅆㅂ|씨발|시발|sibal|cibal|시ㅂ|cㅣ발',
        r'ㅂㅅ|볍신|병ㅅ|byeongshin|병신',
        r'ㄱㅅㄲ|개ㅅㅋ|개색기|gaesaekki|개새끼|개쉐리',
        r'fuck|f[\W_]*u[\W_]*c[\W_]*k',
        r'bitch|b[\W_]*i[\W_]*t[\W_]*c[\W_]*h',
        r'asshole|a[\W_]*s[\W_]*s[\W_]*h[\W_]*o[\W_]*l[\W_]*e',
        r'지랄|꺼져|죽어|뒤져|디져|죽을래',
    ],
    "URL": [
        r'h[\W_]*t[\W_]*t[\W_]*p[s]?[\W_]*://',
        r'(www[\W_]*\.[^\s]+)',
        r'\S+\.com', r'\S+\.net', r'\S+\.kr',
        r'[a-zA-Z0-9\-]{2,}\.[a-z]{2,}(/\S*)?',
        r'dot\s?com', r'dot\s?net',
    ],
    "이메일주소": [
        r'[a-zA-Z0-9_.+-]+\s*(\(at\)|\[at\]|@|＠|골뱅이)\s*[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        r'[a-zA-Z0-9_.+-]+\s*at\s*[a-zA-Z0-9-]+\s*dot\s*[a-zA-Z0-9-.]+',
    ],
    "주민번호": [
        r'\d{6}[-\s]?\d{7}',
    ],
    "카드번호": [
        r'\b(?:\d[ -]*?){13,16}\b',
        r'카드\s?번호\s?:?\s?\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}',
    ],
    "계좌번호": [
        r'\d{2,4}[-\s]?\d{3,6}[-\s]?\d{4,6}',
        r'계좌\s?번호\s?:?\s?\d{3,4}[ -]?\d{3,4}[ -]?\d{4}',
    ],
    "전화번호": [
        r'01[016789]-\d{3,4}-\d{4}',
        r'010\s?\d{4}\s?\d{4}',
        r'0\d{1,2}-\d{3,4}-\d{4}',
        r'0\d{1,2}\s?\d{3,4}\s?\d{4}',
        r'전화\s?번호\s?:?\s?\d{2,4}[-\s]?\d{3,4}[-\s]?\d{4}',
    ],
    "주소": [
        r'(서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주)[^\s,]{1,15}(시|도)',
        r'\d{3,5}\s?(번지|동|호|로|길)',
    ],
    "신용정보": [
        r'cvv\s?\d{3}',
        r'exp\s?\d{2}/\d{2}',
        r'만료일\s?:?\s?\d{2}/\d{2}',
    ],
    "개인정보키워드": [
        r'내\s?이름은', r'내\s?전화', r'내\s?주소', r'내\s?주민번호', r'내\s?계좌', r'내\s?카드',
        r'우리\s?집', r'집주소', r'집\s?전화', r'연락처',
    ],
    "SNS ID": [
        r'카카오톡\s?(아이디|id)\s?:?\s?\S+',
        r'인스타\s?(id|아이디)\s?:?\s?\S+',
        r'텔레그램\s?(id|아이디)\s?:?\s?\S+',
        r'kakao\s?:?\s?\S+',
    ],
}

def check_predefined_patterns(message: str) -> list:
    """
    메시지에서 탐지된 금지 형식 카테고리들을 리스트로 반환
    예: ['욕설', '카드번호']
    """
    detected = []
    for category, patterns in FILTER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                detected.append(category)
                break  # 카테고리당 한 번만 탐지
    return detected
