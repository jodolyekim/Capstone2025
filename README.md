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
# 📱 Heart Spectrum Frontend (Flutter)

신경다양성을 고려한 소개팅 앱의 Flutter 기반 프론트엔드입니다.
회원가입, 로그인, 프로필 설정, 실시간 채팅 기능을 포함하며, 욕설/민감정보 필터링 메시지를 처리할 수 있도록 Django 백엔드와 연동됩니다.

---

## 🚀 실행 방법 (VS Code 기준, Windows)

### 1. Flutter 설치

* [https://docs.flutter.dev/get-started/install/windows](https://docs.flutter.dev/get-started/install/windows) 접속
* SDK 다운로드 후 환경변수 설정까지 마쳐야 함
* VS Code에 Flutter 및 Dart 확장 설치 필요

### 2. Android Emulator 또는 실기기 준비

* Android Studio에서 AVD Manager 실행하여 에뮬레이터 생성 또는
* USB 디버깅을 활성화한 Android 실기기 연결

### 3. 프로젝트 열기 및 의존성 설치

```bash
cd "signup_n_login_ui with chat"
flutter pub get
```

### 4. 앱 실행

```bash
flutter run
```

> 에뮬레이터 또는 연결된 Android 기기에서 실행됨

### 5. API 연동 주소 주의

* 백엔드가 로컬에서 실행 중이라면 Flutter 내에서 주소는 `http://10.0.2.2:8000`으로 설정해야 Android 에뮬레이터에서 접근 가능

---

## 🧩 주요 기능

* ✅ 회원가입 화면 (이메일, 비밀번호 검증 포함)
* ✅ 로그인 화면 (JWT 저장 및 자동 로그인 지원)
* ✅ 프로필 설정 화면 (3단계 입력 방식)
* ✅ 위치 권한 요청 및 거리 슬라이더
* ✅ 실시간 채팅 (WebSocket 기반)
* ✅ 이미지 전송 (채팅 내 사진 업로드 지원)
* ✅ 욕설/민감정보 필터링 결과에 따른 시스템 메시지 표시
* ✅ 프로필 미설정 시 유도 문구/버튼 표시

---

## 📁 주요 폴더 구조 및 파일 설명

```
signup_n_login_ui with chat/
├── android/                 # Android 플랫폼 빌드 관련
├── ios/                     # iOS 플랫폼 빌드 관련
├── lib/
│   ├── chat/                # 채팅 관련 기능 분리 폴더
│   │   ├── chat_screen.dart      # 실시간 채팅 UI 화면
│   │   └── chat_service.dart     # WebSocket 연결/전송 로직
│   ├── landing_page.dart    # 초기 진입: 로그인/회원가입 선택
│   ├── login_page.dart      # 로그인 화면
│   ├── main.dart            # 앱 진입점
│   ├── profile_setup.dart   # 3단계 프로필 입력 UI
│   └── signup_page.dart     # 회원가입 UI
├── pubspec.yaml             # 의존성 정의 파일
├── pubspec.lock             # 실제 설치된 패키지 잠금
├── README.md                # 설명 문서
```

---

## 📦 주요 의존성 (`pubspec.yaml`)

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.6
  image_picker: ^1.0.4
  shared_preferences: ^2.2.1
  web_socket_channel: ^2.4.0
```

---

## 📡 서버 연동 정보

| 항목      | 값                                 |
| ------- | --------------------------------- |
| 백엔드 주소  | `http://10.0.2.2:8000` (에뮬레이터 기준) |
| 로그인 방식  | JWT (Authorization 헤더에 저장)        |
| 이미지 업로드 | `multipart/form-data` POST 방식     |
| 채팅 방식   | WebSocket (Django Channels 기반)    |

---

## 🛠 기타 팁

* 이미지 전송 실패 시 시스템 메시지로 사용자에게 알림 표시됨
* 필터링에 걸린 채팅은 전송되지 않으며, 서버에서 SYSTEM 메시지로 사유를 알려줌
* 모든 상태값은 로컬 SharedPreferences에 저장되어 재로그인 방지 가능
* 각 화면은 기능별로 파일이 분리되어 있어 유지보수에 용이함

---

> Flutter 관련 문제 발생 시 `flutter doctor` 명령어로 환경을 점검하세요.
