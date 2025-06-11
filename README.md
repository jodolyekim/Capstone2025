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
├── .env                  # 환경변수 configuration (.gitignore로 포함 안됨)Add commentMore actions
├── .gitignore            # 보안상 중요한 파일(ex: .env, db.splite3 등)은 Github에 푸시할 때 무시하도록
├── Dockerfile            # Docker image 생성을 위한 스크립트 파일
├── docker-compose.yml    # Docker 컨테이너 서비스 정의 및 프로젝트 수행 파일
├── requirements.txt      # 프로젝트에 요구되는 라이브러리 및 프레임워크 의존성 목록
├── db.sqlite3            # Django Database (.gitignore로 포함 안됨)
├── docker-compose.yml
├── project_structure.txt
├── requirements.txt
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
├── users
├── interest
├── matching
├── chat
├── photos
└── sms
```



### 상세
```
├── check_models.py
├── chat
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   │   └── __init__.py
│   ├── models.py
│   ├── routing.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils
│   │   ├── gpt_judge.py
│   │   ├── message_filtering.py
│   │   └── message_restriction.py
│   └── views.py
├── interest
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── gpt_utils.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── matching
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── photos
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── firebase.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── sms
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── sms_real.py
│   ├── test_sms.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── backends.py
    ├── management
    │   ├── __init__.py
    │   └── commands
    │       ├── __init__.py
    │       ├── create_fortest_users.py
    │       └── create_keywords.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_rename__birthymd_profile_birth_date_and_more.py
    │   ├── 0003_delete_interest_alter_profile_interests.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

### 정적 파일
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
