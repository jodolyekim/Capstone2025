# 캡스톱 프로젝트 최종 결과물

## 디렉토리 구조
main 브랜치에 backend와 frontend 디렉토리를 생성하고 분류했습니다.

### backend
for Django Projects & Docker Container Configuration
```bash
backend
├── .env                  # 환경변수 configuration 
├── .gitignore
├── Dockerfile            # Docker Conatiner configuration
├── config
│   ├── asgi.py
│   ├── settings.py       # 
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3            # Django Database (.gitignore로 포함 안됨)
├── docker-compose.yml
├── project_structure.txt
├── requirements.txt
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
├── check_models.py
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
├── manage.py
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


### frontend
```bash

```
