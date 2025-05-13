from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 기본 관리자 페이지

    path('api/', include('users.urls')),  # 사용자 관련 API (회원가입, 로그인 등)
    path('api/chat/', include('chat.urls')),  # ✅ chat 관련 API 라우팅 추가
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT access/refresh 토큰 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh 토큰을 이용한 access 재발급
]

# 개발 환경일 때만 미디어 파일 서빙 허용
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)