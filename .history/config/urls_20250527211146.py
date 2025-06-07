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
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/alerts/', include('alerts.urls')),
    path("api/interest/", include("interest.urls")),
    path('api/photos/', include('photos.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# 개발 환경에서만 static/media 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
