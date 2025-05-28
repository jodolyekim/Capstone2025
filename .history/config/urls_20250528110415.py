# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ✅ 관리자 페이지
    path('admin/', admin.site.urls),

    # ✅ 사용자 관련 API (회원가입, 로그인, 프로필, 매칭, 보호자, 관심사)
    path('api/', include('users.urls')),

    # ✅ 채팅 기능
    path('api/chat/', include('chat.urls')),

    # ✅ 알림 기능
    path('api/alerts/', include('alerts.urls')),

    # ✅ 사진 업로드
    path('api/photos/', include('photos.urls')),

    # ✅ JWT 인증
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# ✅ 개발 환경에서 정적 및 미디어 파일 직접 제공
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
