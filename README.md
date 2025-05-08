# Capstone2025
Dankook Univ. Capstone Project 2025 1st semester.

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
