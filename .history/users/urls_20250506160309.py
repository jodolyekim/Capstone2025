from django.urls import path
from .views import SignupView, ProfileView, CustomTokenObtainPairView, CurrentUserView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),             # 회원가입
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 🔥 이거 수정!
    path('profile/', ProfileView.as_view(), name='profile'),          # 프로필
    path('me/', CurrentUserView.as_view(), name='me'),                # 현재 로그인 유저
]
