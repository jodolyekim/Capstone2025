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

    # ✅ 사용자 인증 및 유저 관련 API
    path('api/', include('users.urls')),
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 💬 채팅
    path('api/chat/', include('chat.urls')),

    # 🔔 보호자 알림 (문자 발송)
    path('api/sms/', include('sms.urls')),

    # 🖼️ 사진 업로드
    path('api/photos/', include('photos.urls')),

    # 🎯 관심사
    path('api/interest/', include('interest.urls')),

    # 🤝 매칭
    path('api/match/', include('matching.urls')),
]

# ✅ 개발 환경에서 static/media 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
