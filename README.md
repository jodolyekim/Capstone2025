# Capstone2025
Dankook Univ. Capstone Project 2025 1st semester.

<<<<<<< HEAD
# 📝 Heart Spectrum Backend (Django)

신경다양성을 고려한 소개팅 앱의 백엔드입니다. Django 기반으로 구축되었으며, 회원가입, 로그인, 프로필 설정, 실시간 채팅, 욕설/민감정보 필터링 기능을 포함합니다.

---

## 🚀 실행 방법 (VS Code 기준, Windows)

### 1. Python 설치

* [https://www.python.org/downloads/](https://www.python.org/downloads/) 접속 후 Python 3.10 이상 설치
* 설치 시 **"Add Python to PATH" 반드시 체크**

### 2. Redis 설치

* Windows: [https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases)
* 설치 후 `redis-server.exe` 실행

### 3. VS Code에서 프로젝트 열기

* `signup_n_login_back with chat/` 폴더를 통째로 VS Code에서 열기

### 4. 가상환경 생성

```bash
python -m venv venv
```

### 5. 가상환경 활성화

```bash
venv\Scripts\activate
```

(터미널에 `(venv)` 표시되면 성공)

### 6. 의존성 패키지 설치 (한 줄 명령어로)

```bash
pip install -r requirements.txt
```

> 위 명령을 실행하면 아래 모든 패키지가 자동 설치됩니다.

### 7. `.env` 파일 생성 (같은 디렉토리에 직접 생성)

```env
OPENAI_API_KEY=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
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

> ⚠️ 이 파일은 `.gitignore`에 포함되어야 하며, 외부에 노출되면 안 됩니다.

### 8. 마이그레이션 적용

```bash
python manage.py migrate
```

### 9. 관리자 계정 생성 (이미 생성된 경우 생략)

* 기본 관리자 계정:

  * 이메일: `amaryllis@naver.com`
  * 비밀번호: `amaryrllis1234`

### 10. Daphne 서버 실행 (WebSocket 포함)

```bash
daphne -p 8000 config.asgi:application
```

서버가 정상적으로 실행되면 `http://127.0.0.1:8000` 또는 `http://localhost:8000` 에서 확인 가능

---

## 🧩 주요 기능

* ✅ 회원가입, 로그인 (JWT 기반)
* ✅ 프로필 설정 (성별, 출생일, 거리 범위)
* ✅ 채팅 기능 (WebSocket 실시간 통신)
* ✅ 사진 전송 기능 (채팅 중 이미지 업로드 가능)
* ✅ 욕설 및 민감정보 필터링 (정규식 + GPT API)
* ✅ Redis 기반 채널 통신
* ✅ 관리자 페이지:

  * 전체 채팅 기록 조회 가능
  * 필터링에 의해 차단된 채팅 내용도 확인 가능

---

## 📂 폴더/파일 설명

### 📁 `chat/` 앱

실시간 채팅 기능과 필터링 시스템을 담당하는 핵심 앱입니다.

| 경로             | 설명                                              |
| -------------- | ----------------------------------------------- |
| `apps.py`      | Django 앱 설정                                     |
| `models.py`    | 채팅 메시지, 시스템 메시지, 필터링 로그 등의 데이터베이스 모델 정의         |
| `consumers.py` | WebSocket 연결을 비동기로 처리하는 핵심 로직 (Django Channels) |
| `views.py`     | 이미지 업로드 등 HTTP 기반 API 처리                        |
| `routing.py`   | WebSocket용 라우팅 설정 (ASGI 기반)                     |
| `urls.py`      | 일반 REST API용 URL 라우팅                            |
| `admin.py`     | Django 관리자 페이지에 모델 등록                           |
| `tests.py`     | 단위 테스트 모듈                                       |

### 📁 `chat/utils/`

욕설 필터링 및 GPT 판단 로직이 들어 있는 유틸리티 폴더입니다.

| 경로                     | 설명                            |
| ---------------------- | ----------------------------- |
| `gpt_judge.py`         | GPT API를 호출해 민감한 메시지를 판단하는 로직 |
| `message_filtering.py` | 정규표현식을 통한 기본적인 형식 필터링 로직      |

### 📁 `config/`

Django 전체 프로젝트 설정 디렉토리입니다.

| 경로            | 설명                             |
| ------------- | ------------------------------ |
| `settings.py` | 전체 환경설정 파일, 앱 등록 및 DB 설정 포함    |
| `urls.py`     | 최상위 URL 라우터                    |
| `asgi.py`     | WebSocket 처리용 ASGI 설정 진입점      |
| `wsgi.py`     | WSGI 서버 설정 진입점 (일반 HTTP 서버 용도) |

---

## 📦 requirements.txt 패키지 목록

```txt
asgiref==3.8.1
attrs==25.3.0
autobahn==24.4.2
Automat==25.4.16
cffi==1.17.1
channels==4.2.2
channels_redis==4.2.1
constantly==23.10.4
cryptography==44.0.3
daphne==4.1.2
Django==5.2
django-cors-headers==4.7.0
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
hyperlink==21.0.0
idna==3.10
incremental==24.7.2
msgpack==1.1.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pycparser==2.22
PyJWT==2.9.0
pyOpenSSL==25.0.0
redis==6.0.0
service-identity==24.2.0
setuptools==80.4.0
sqlparse==0.5.3
Twisted==24.11.0
txaio==23.1.1
typing_extensions==4.13.2
tzdata==2025.2
zope.interface==7.2
openai==0.28.0
python-dotenv
pillow
```

---

## 🔧 설치해야 하는 외부 프로그램 요약

| 항목     | 설명                 |
| ------ | ------------------ |
| Python | 3.10 이상, pip 포함    |
| Redis  | 채팅 기능용 pub/sub 백엔드 |
| Git    | 프로젝트 버전 관리 (선택)    |
| Daphne | ASGI 서버 실행용        |

---

## 📡 기술 스택 요약

| 구성 요소           | 사용 여부 |
| --------------- | ----- |
| Django          | ✅     |
| Django Channels | ✅     |
| WebSocket       | ✅     |
| Redis           | ✅     |
| REST API        | ✅     |
| GPT API 필터링     | ✅     |
| Daphne (ASGI)   | ✅     |

---

> 문의나 협업 제안은 GitHub Issues 또는 Pull Request를 통해 주세요.
=======
⚙️ Django (백엔드)
🔹 주요 앱 및 구조
앱 이름: users

사용자 모델: CustomUser (이메일 로그인 기반)

프로필 모델: Profile (OneToOne 관계)

추가 모델: Guardian, Photo, Interest, Match, ChatRoom 등

🔸 구현된 기능
✅ 회원가입 (/api/signup/)
이메일, 비밀번호, 비밀번호 확인 입력

비밀번호 불일치, 이메일 중복 등 오류 메시지 한글 제공

가입 완료 시 JWT 토큰 발급

✅ 로그인 (/api/login/)
이메일 + 비밀번호 기반 로그인

실패 시 오류 메시지를 항목별로 한글로 반환

✅ 프로필 API
GET /api/profile/: 로그인 사용자의 프로필 전체 조회

PATCH /api/profile/update/: 프로필 단계별 업데이트 처리

설정된 필드가 모두 입력되면 is_profile_set 자동 True

✅ 인증/보안
JWT 인증 (rest_framework_simplejwt)

이메일 로그인 커스텀 인증 백엔드 적용

CORS 허용 (Flutter와의 연동 위해 설정 완료)

🧪 개발 환경
Flutter SDK: 3.x

Django: 5.x

의존성:

shared_preferences

http

geolocator

image_picker

django-cors-headers

rest_framework, rest_framework_simplejwt
>>>>>>> feature/alerts-photo-notification
