from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    save_or_update_profile,
    GuardianCreateView,
    GuardianUploadView
)

urlpatterns = [
    # 회원가입 엔드포인트
    path('signup/', SignupView.as_view(), name='signup'),

    # JWT 로그인 엔드포인트
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 로그인한 사용자의 프로필 조회/수정
    path('profile/', ProfileView.as_view(), name='profile'),

    # 현재 로그인한 사용자 정보 반환 (예: 이메일, user_id 등)
    path('me/', CurrentUserView.as_view(), name='me'),

    # Flutter에서 단계별 프로필 저장 요청 처리 (PATCH 방식)
    path('profile/update/', save_or_update_profile, name='profile_update'),

    # 보호자 라우터
    path('guardian/create/', GuardianCreateView.as_view(), name='guardian-create'),
    path('guardian/upload/', GuardianUploadView.as_view()),
]
