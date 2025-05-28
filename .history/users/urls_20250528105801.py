from django.urls import path
from . import views  # ✅ 전체 views 모듈을 import해서 views.함수명으로 사용

urlpatterns = [
    # ✅ 인증 및 프로필
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('me/', views.CurrentUserView.as_view(), name='me'),
    path('profile/update/', views.save_or_update_profile, name='profile_update'),
    path('profile/set-complete/', views.MarkProfileCompleteView.as_view(), name='profile_complete'),

    # ✅ 보호자
    path('guardian/create/', views.GuardianCreateView.as_view(), name='guardian-create'),
    path('guardian/upload/', views.GuardianUploadView.as_view(), name='guardian-upload'),

    # ✅ 매칭
    path('match/candidates/', views.get_candidates, name='match-candidates'),
    path('api/match/respond/', views.respond_to_match, name='match-respond'),
    path('api/initiate/', views.initiate_match, name='initiate-match'),  # ✅ 핵심 추가

    # ✅ 관심사 (GPT/수동/추천)
    path('interest/manual/', views.save_manual_interest, name='interest-manual'),
    path('interest/save/', views.save_gpt_interest, name='interest-gpt-save'),
    path('interest/manual-keywords/', views.get_manual_interest_keywords, name='interest-manual-keywords'),
    path('interest/suggestions/', views.get_suggested_interests, name='interest-suggestions'),
]
