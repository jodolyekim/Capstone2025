# 캡스톱 프로젝트 최종 결과물

## 디렉토리 구조
main 브랜치에 backend와 frontend 디렉토리를 생성하고 분류했습니다.

## backend

### 사용한 기술 스택
```

```

### 전체 Django 프로젝트와 Docker 컨테이너 환경 설정 디렉토리
```
backend
├── .env                  # 환경변수 configuration (.gitignore로 포함 안됨)
├── .gitignore            # 보안상 중요한 파일(ex: .env, db.splite3 등)은 Github에 푸시할 때 무시하도록
├── Dockerfile            # Docker image 생성을 위한 스크립트 파일
├── docker-compose.yml    # Docker 컨테이너 서비스 정의 및 프로젝트 수행 파일
├── requirements.txt      # 프로젝트에 요구되는 라이브러리 및 프레임워크 의존성 목록
├── db.sqlite3            # Django Database (.gitignore로 포함 안됨)
├── manage.py             # Django 프로젝트 실행 파일
└── config                # Django 프로젝트 최상위 루트 configuration
    ├── asgi.py
    ├── settings.py       
    ├── urls.py
    └── wsgi.py
```


### 구현한 애플리케이션 백엔드 기능 디렉토리
프로젝트에서 구현한 애플리케이션 기능에 해당하는 Django 프로젝트 디렉토리

---

### 요약
```
...
├── users      # 사용자 관련 
├── interest   # 관심사 설정
├── matching   # 매칭 
├── chat       # 채팅
├── photos     # 사진 는 실제 저장한 사진 파일이 저장되는 디렉토리
```
├── media
│   ├── chat_images
│   │   └── 42.jpg
│   ├── guardian
│   │   ├── disability_1_42.jpg
│   │   ├── disability_21_43.jpg
│   │   ├── disability_22_42.jpg
│   │   ├── disability_23_42.jpg
│   │   ├── family_1_43.jpg
│   │   ├── family_21_42.jpg
│   │   ├── family_22_43.jpg
│   │   └── family_23_43.jpg
│   └── profile_photos
│       ├── 42.jpg
│       ├── 42_23gybBq.jpg
│       ├── 42_P0t5heN.jpg
│       ├── 42_UzdbJQL.jpg
│       ├── 42_sdf2bqy.jpg
│       ├── 43.jpg
│       ├── 43_8jDyiAA.jpg
│       ├── 43_kNlBhMr.jpg
│       ├── 43_rURwhrH.jpg
│       └── test_image.jpg
└── staticfiles
```


### frontend
```
frontend
├── lib
│   ├── afterloginmain
│   │   ├── chat_room_list_screen
│   │   └── family_23_43.jpg
│   ├── screens
│   ├── services
│   ├── Widgets
│   └── main.dart
└── pubspec.yaml
```
