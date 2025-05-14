import os
from pathlib import Path
from datetime import timedelta

# 기본 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 설정
SECRET_KEY = 'django-insecure-ykz*hh-f%1*deiuzu#x#blt@0zi0y2$g%95beccq27^o6ona6!'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.2.2']

# 앱 설정
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'chat',        # ✅ 채팅 앱
    'channels',    # ✅ Django Channels (WebSocket 처리)
]

# CORS 설정 - Flutter와의 연동을 위한 도메인 허용
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",
    "http://localhost:8000",
    "http://10.0.2.2:8000",
]

# 미들웨어 설정
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL 설정
ROOT_URLCONF = 'config.urls'

# 템플릿 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 설정
WSGI_APPLICATION = 'config.wsgi.application'

# ✅ ASGI 설정 (WebSocket용)
ASGI_APPLICATION = 'config.asgi.application'

# ✅ Redis 기반 Channels 설정
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 국제화 설정
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ 정적 파일 및 미디어 파일 설정
STATIC_URL = 'static/'

# ✅ 미디어 파일 관련 설정 (이미지 업로드 기능에 필요)
MEDIA_URL = '/media/'  # 브라우저에서 접근하는 URL prefix
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 서버에 실제 저장될 디렉토리

# 기본 필드 타입
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 사용자 모델 커스터마이징
AUTH_USER_MODEL = 'users.CustomUser'

# 인증 백엔드 설정
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# REST 프레임워크 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# JWT 토큰 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
