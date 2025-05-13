# 라우팅 최상위(root) 레벨
# 사용자 인증, 관심사, 수동 키워드 선택, 매칭, 사진 업로드
from django.contrib import admin
from django.urls import path, include
from django.conf import settings                # settings import 수정
from django.conf.urls.static import static      # static import 추가
from rest_framework_simplejwt.views import (    
    TokenObtainPairView, 
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),                                                # Django 기본 관리자 페이지
    path('api/', include('users.urls')),                                            # 사용자 관련 API (회원가입, 로그인, 매칭 등)
    path("api/interest/", include("interest.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # JWT access/refresh 토큰 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # refresh 토큰을 이용한 access 재발급
    path('photos/', include('photos.urls')),                                        # 사진 업로드
]

# 개발 환경일 때만 미디어 파일 서빙 허용
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)