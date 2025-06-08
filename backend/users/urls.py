from django.urls import path
from . import views  # ✅ 전체 views 모듈을 import해서 views.함수명으로 사용

urlpatterns = [
    # ✅ 사용자 인증 및 프로필 관련
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('me/', views.CurrentUserView.as_view(), name='me'),
    path('profile/update/', views.save_or_update_profile, name='profile_update'),
    path('profile/set-complete/', views.MarkProfileCompleteView.as_view(), name='profile_complete'),

    # ✅ 보호자 정보 관련
    path('guardian/create/', views.GuardianCreateView.as_view(), name='guardian-create'),
    path('guardian/upload/', views.GuardianUploadView.as_view(), name='guardian-upload'),
]
