import re

# 사전 정의된 금칙어 및 민감정보 형식 패턴
FILTER_PATTERNS = {
    "욕설": [
        r'ㅅ+ㅂ|ㅆㅂ|씨+발|시발|c[i1]bal|tlqkf',
        r'ㅂㅅ|볍신|병신|븅신|qkfxl|wls',
        r'ㄱㅅㄲ|개ㅅㅋ|개색기|개새끼|개쉐리|gaesaekki|g[a4]esa[e3]kki',
        r'지랄|ㅈㄹ|zlral|g랄',
        r'존나|ㅈㄴ|좆나|조낸|쫀나',
        r'좆[가-힣]*|좇[가-힣]*|x까|좆같|좆ㄱㅏ',
        r'fuck|f[\W_]*u[\W_]*c[\W_]*k|fck|f\*ck|fcuk',
        r'sh[i1]t|s#it|s\*it',
        r'b[i!*]tch|bi7ch|b\*tch',
        r'a[s$]{2}hole|ass\s?h0le|a\$hole',
        r'motherf[\W_]*\*?ker|mofo|bastard|slut|pussy|cunt|fag|retard',
        r'n[i1!]{1,2}gg[a@]?',
        r'꺼져|죽어|뒤져|디져|죽을래|엿\s?먹|개소리|미친X|ㅁㅊㄴ|ㅄ',
        r'느[금급]마|니애미|엄마좆|엄마X',
        r'[가-힣]{2,}(충|츙)',
    ],

    "URL": [
        r'(h[\W_]*t[\W_]*t[\W_]*p[s]?[\W_]*:\/\/)|(www[\W_]*\.[^\s]+)',
        r'\S+\.com|\S+\.net|\S+\.kr|\S+\.(org|co|shop|tv)',
        r'[a-zA-Z0-9\-]{2,}\.[a-z]{2,}(/\S*)?',
        r'dot\s?(com|net|kr)',
    ],

    "이메일주소": [
        r'[0-9A-Za-z._%+-]+\s*(\(at\)|\[at\]|@|＠|골뱅이)\s*[0-9A-Za-z.-]+\.[A-Za-z]{2,}',
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
        r'01[016789][-]?\d{3,4}[-]?\d{4}',
        r'0\d{1,2}[-]?\d{3,4}[-]?\d{4}',
        r'공\s?일\s?공|공\s?이\s?오|영\s?일\s?영|0IO|zero one zero',
    ],

    "주소": [
        r'(서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주).{0,10}(시|도|구|군)',
        r'\d{1,5}\s?(번지|동|호|로|길)',
    ],

    "신용정보": [
        r'cvv\s?\d{3}',
        r'exp\s?\d{2}/\d{2}',
        r'만료일\s?:?\s?\d{2}/\d{2}',
    ],

    "개인정보키워드": [
        r'내\s?(이름|전화|주소|주민번호|계좌|카드)',
        r'우리\s?집|집주소|집\s?전화|연락처',
    ],

    "SNS ID": [
        r'(카카오톡|카톡|kakao)\s?(아이디|ID)?\s?:?\s?\S+',
        r'(인스타|instagram|insta)\s?(아이디|ID)?\s?:?\s?\S+',
        r'(디스코드|디코|discord)\s?(아이디|ID)?\s?:?\s?\S+',
        r'(텔레그램|텔레|telegram)\s?(아이디|ID)?\s?:?\s?\S+',
        r'(페이스북|페북|facebook|fb)\s?(아이디|ID)?\s?:?\s?\S+',
        r'@[\w.]+|#\d{4}',
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
                break
    return detected
