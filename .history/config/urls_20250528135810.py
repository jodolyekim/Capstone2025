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
    path('admin/', admin.site.urls),

    # ✅ 사용자 관련 API
    path('api/', include('users.urls')),

    # ✅ 채팅
    path('api/chat/', include('chat.urls')),

    # ✅ 알림
    path('api/alerts/', include('alerts.urls')),

    # ✅ 사진
    path('api/photos/', include('photos.urls')),

    # ✅ 관심사
    path('api/interest/', include('interest.urls')),  # ✅ 이 줄 추가 필수

    # ✅ JWT 인증
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
