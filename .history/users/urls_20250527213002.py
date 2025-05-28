from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    save_or_update_profile,
    GuardianCreateView,
    GuardianUploadView,
    MarkProfileCompleteView,
    get_candidates,
    respond_to_match,
    save_manual_interest      # ✅ 관심사 저장 API 추가
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('profile/update/', save_or_update_profile, name='profile_update'),
    path('profile/set-complete/', MarkProfileCompleteView.as_view(), name='profile_complete'),

    # ✅ 보호자 관련
    path('guardian/create/', GuardianCreateView.as_view(), name='guardian-create'),
    path('guardian/upload/', GuardianUploadView.as_view()),

    # ✅ 매칭 관련
    path('match/candidates/', get_candidates, name='match-candidates'),
    path('match/respond/<int:match_id>/', respond_to_match, name='match-respond'),

    # ✅ 관심사 저장
    path('interest/manual/', save_manual_interest, name='interest-manual'),  # 💡 이 줄 추가
]
