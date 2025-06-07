from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 🔐 관리자
    path('admin/', admin.site.urls),

    # ✅ 사용자 관련 API
    path('api/', include('users.urls')),
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 💬 채팅 기능
    path('api/chat/', include('chat.urls')),

    # 🔔 보호자 문자 발송 기능 (alerts → sms로 변경됨)
    path('api/sms/', include('sms.urls')),

    # 🖼️ 사진 업로드
    path('api/photos/', include('photos.urls')),

    # 🎯 관심사 및 추천
    path('api/interest/', include('interest.urls')),

    # 🤝 매칭 기능
    path('api/match/', include('matching.urls')),
]

# 개발 모드에서 static/media 파일 제공
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
