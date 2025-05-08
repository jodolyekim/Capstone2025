from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    update_profile_partial,  # ✅ 추가된 부분
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 로그인
    path('profile/', ProfileView.as_view(), name='profile'),  # 프로필 조회/수정
    path('me/', CurrentUserView.as_view(), name='me'),  # 현재 로그인한 사용자 정보
    path('profile/update/', update_profile_partial, name='profile_update'),  # ✅ Flutter용 프로필 부분 업데이트
]
