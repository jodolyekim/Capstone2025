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

# Heart Spectrum Frontend (Flutter)

신경다양성을 고려한 소개팅 앱의 Flutter 기반 프론트엔드입니다.  
회원가입, 로그인, 프로필 설정, 실시간 채팅 기능을 포함하며, 욕설/민감정보 필터링 메시지를 처리할 수 있도록 Django 백엔드와 연동됩니다.

---

## 🚀 실행 방법 (VS Code 기준, Windows)

1. Flutter 설치  
   - https://docs.flutter.dev/get-started/install/windows  
   - 환경변수 설정 필수 (`flutter doctor`로 점검)

2. Android Emulator 또는 실기기 준비  
   - Android Studio AVD 또는 USB 디버깅된 기기 연결

3. 프로젝트 열기 및 의존성 설치

```bash
cd "signup_n_login_ui with chat and guardian"
flutter pub get
```

4. 앱 실행

```bash
flutter run
```

> 에뮬레이터 또는 연결된 기기에서 앱이 실행됨

5. 백엔드 API 주소 설정  
   - Android 에뮬레이터에서 Django 서버에 접근하려면 주소는 `http://10.0.2.2:8000` 로 설정해야 함

---

## ✅ 주요 기능

- 회원가입 (이메일 형식 및 비밀번호 검증)
- 로그인 (JWT 저장, 자동 로그인)
- 3단계 프로필 입력
- 위치 권한 요청 + 거리 범위 슬라이더
- 실시간 채팅 (WebSocket)
- 이미지 전송 (사진 업로드)
- 욕설/민감정보 필터링 → 시스템 메시지로 알림
- 프로필 미설정 시 안내 메시지 + 버튼 표시
- ✅ 보호자 정보 입력 UI (이름, 관계, 생년월일, 전화번호 입력)

---

## 📁 주요 폴더 구조

```
signup_n_login_ui with chat and guardian/
├── lib/
│   ├── chat/
│   │   ├── chat_screen.dart         # 실시간 채팅 UI
│   │   └── chat_service.dart        # WebSocket 통신
│   ├── guardian.dart                # 보호자 정보 입력 화면
│   ├── landing_page.dart            # 로그인/회원가입 선택
│   ├── login_page.dart              # 로그인 UI
│   ├── main.dart                    # 앱 진입점
│   ├── profile_setup.dart           # 3단계 프로필 설정
│   └── signup_page.dart             # 회원가입 UI
├── pubspec.yaml
```

---

## 📦 주요 의존성 (`pubspec.yaml`)

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.6
  shared_preferences: ^2.2.1
  web_socket_channel: ^2.4.0
  image_picker: ^1.0.4
  geolocator: ^10.1.0
```

---

## 📡 서버 연동 정보

| 항목            | 설명                                       |
|-----------------|--------------------------------------------|
| 백엔드 주소       | `http://10.0.2.2:8000` (Android 에뮬레이터 기준) |
| 로그인 방식       | JWT (SharedPreferences에 저장됨)               |
| 채팅 방식         | WebSocket (Django Channels)                 |
| 이미지 업로드     | `multipart/form-data` 방식으로 전송              |
| 필터링 결과 처리    | SYSTEM 메시지로 차단 사유 안내                    |

---

## 💡 기타

- `flutter doctor`로 환경 점검 가능
- 앱 상태값은 SharedPreferences에 저장되며 로그인 유지됨
- 채팅 필터링에 걸리면 메시지 전송되지 않고 사유를 알림으로 표시

---

> 문의나 피드백은 GitHub Issues 또는 Pull Request로 남겨주세요.
