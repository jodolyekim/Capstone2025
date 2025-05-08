# signup_n_login_ui

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

📱 Flutter (프론트엔드)
🔹 전체 구조
main.dart: 앱 진입점, 라우팅 설정 포함

화면 구성: LandingPage, LoginPage, SignupPage, ProfileSetupScreen

🔸 구현된 기능
✅ 랜딩 페이지 (LandingPage)
앱 이름 표시

로그인 및 회원가입 버튼

✅ 로그인 페이지 (LoginPage)
이메일/비밀번호 입력

JWT 로그인 요청

로그인 성공 시 프로필 설정 여부 확인

프로필이 설정되지 않은 경우, 프로필 설정 화면으로 안내

백엔드 오류 메시지 한글 표시 처리

✅ 회원가입 페이지 (SignupPage)
이름, 이메일, 비밀번호 입력

비밀번호 확인 일치 여부 체크

회원가입 성공 시 프로필 설정 이동 유도

✅ 프로필 설정 (ProfileSetupScreen)
3단계 단계별 입력 및 서버 저장

1단계: 이름, 생년월일, 성별, 성적 지향

2단계: 선호하는 대화 방식 (복수 선택 가능)

3단계: 현재 위치 요청 및 매칭 거리 슬라이더 설정

각 단계 완료 시 Django 서버에 PATCH 요청하여 정보 저장

SharedPreferences를 통해 토큰 저장 및 활용
