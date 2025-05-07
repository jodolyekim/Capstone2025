from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ JWT import 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # users 앱의 signup, profile 등 API
    
    # ✅ JWT 토큰 엔드포인트 추가
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
