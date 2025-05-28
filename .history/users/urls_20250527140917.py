from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    save_or_update_profile,
    GuardianCreateView,
    GuardianUploadView,
    MarkProfileCompleteView  # ✅ 추가
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('profile/update/', save_or_update_profile, name='profile_update'),

    # ✅ 관심사 입력 완료 후 계정 활성화
    path('profile/set-complete/', MarkProfileCompleteView.as_view(), name='profile_complete'),

    # 보호자 관련
    path('guardian/create/', GuardianCreateView.as_view(), name='guardian-create'),
    path('guardian/upload/', GuardianUploadView.as_view()),
]
