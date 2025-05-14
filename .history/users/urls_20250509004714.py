from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    save_or_update_profile,  # ✅ 이름 변경된 함수로 수정
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 로그인
    path('profile/', ProfileView.as_view(), name='profile'),  # 프로필 조회/수정
    path('me/', CurrentUserView.as_view(), name='me'),  # 현재 로그인한 사용자 정보
    path('profile/update/', save_or_update_profile, name='profile_update'),  # ✅ 단계별 프로필 저장
]
