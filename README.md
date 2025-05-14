# Capstone2025
Dankook Univ. Capstone Project 2025 1st semester.
# Capstone2025

Dankook Univ. Capstone Project 2025 1st semester.

---

# 📝 Heart Spectrum Backend (Django)

신경다양성을 고려한 소개팅 앱의 백엔드입니다. Django 기반으로 구축되었으며, 회원가입, 로그인, 프로필 설정, 실시간 채팅, 욕설/민감정보 필터링, 보호자 인증 기능을 포함합니다.

---

## 🚀 실행 방법 (VS Code 기준, Windows)

1. Python 설치  
   - https://www.python.org/downloads/ 에서 Python 3.10 이상 설치  
   - 설치 시 "Add Python to PATH" 체크 필수

2. Redis 설치  
   - Windows용 Redis: https://github.com/tporadowski/redis/releases  
   - 설치 후 `redis-server.exe` 실행

3. 프로젝트 열기  
   - `signup_n_login_back with chat and guardian/` 폴더를 VS Code로 열기

4. 가상환경 생성 및 활성화

```bash
python -m venv venv
venv\Scripts\activate
```

5. 패키지 설치

```bash
pip install -r requirements.txt
```

6. `.env` 파일 생성

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

7. 마이그레이션 적용

```bash
python manage.py migrate
```

8. 관리자 계정 생성

```bash
python manage.py createsuperuser
```

9. Daphne 실행 (WebSocket 포함)

```bash
daphne -p 8000 config.asgi:application
```

---

## ✅ 주요 기능

- 회원가입 및 JWT 로그인
- 프로필 설정 (성별, 출생일, 거리 범위 등)
- 실시간 채팅 (WebSocket)
- 이미지 전송 기능
- 욕설/민감정보 형식 필터링 + GPT API 필터링
- 관리자 페이지 전체 채팅 로그 확인 가능
- ✅ 보호자 정보 입력 및 검토 기능
  - 보호자 이름, 전화번호, 생년월일, 관계 입력
  - 가족관계증명서 및 장애인등록증 이미지 업로드
  - 관리자가 수동 승인 (미승인 시 로그인 불가)

---

## 📁 앱 구조

### `users/`
- 사용자 모델: `CustomUser` (이메일 로그인 기반)
- 프로필 모델: `Profile` (OneToOne)
- 보호자 모델: `Guardian`
- 기타 모델: `Photo`, `Interest`, `Match`, `ChatRoom`

### `chat/`
- 채팅 메시지, 시스템 메시지, 필터링 로그
- `consumers.py`: WebSocket 처리
- `utils/message_filtering.py`: 정규식 필터
- `utils/gpt_judge.py`: GPT API 판단

---

## 📦 requirements.txt 예시

```txt
Django==5.2
djangorestframework
djangorestframework_simplejwt
channels
channels_redis
daphne
redis
openai
python-dotenv
pillow
```

---

## 🔧 외부 의존

| 항목     | 설명                              |
|--------|---------------------------------|
| Python | 3.10 이상, pip 포함                   |
| Redis  | 채팅 pub/sub용                      |
| Daphne | WebSocket 서버                        |
| OpenAI | 욕설/민감정보 필터링 판단용 GPT API 키 필요 |

---

## 📡 기술 요약

| 기술 요소         | 사용 여부 |
|------------------|----------|
| Django           | ✅        |
| Django Channels  | ✅        |
| Redis            | ✅        |
| Daphne (ASGI)    | ✅        |
| REST API         | ✅        |
| GPT 필터링        | ✅        |
| 이미지 업로드      | ✅        |
| 관리자 승인 기능    | ✅        |
