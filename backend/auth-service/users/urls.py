from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    CustomTokenObtainPairView,
    CurrentUserView,
    save_or_update_profile,
)

from .views_interest import (
    ManualKeywordSaveView,
    ManualKeywordRecommendationView,
    DeleteKeywordView,
    GPTKeywordExtractionView,
    GPTKeywordSaveView,
    UserKeywordListView,
)

urlpatterns = [
    # 회원가입 엔드포인트
    path('signup/', SignupView.as_view(), name='signup'),

    # JWT 로그인 엔드포인트
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 로그인한 사용자의 프로필 조회/수정
    path('profile/', ProfileView.as_view(), name='profile'),

    # 현재 로그인한 사용자 정보 반환
    path('me/', CurrentUserView.as_view(), name='me'),

    # 프로필 단계별 저장
    path('profile/update/', save_or_update_profile, name='profile_update'),

    # GPT 키워드 추출 및 저장
    path('interests/extract/', GPTKeywordExtractionView.as_view(), name='extract_keywords'),
    path('interests/save/', GPTKeywordSaveView.as_view(), name='save_keywords'),

    # 수동 키워드 추천/저장/삭제
    path('interests/manual/recommend/', ManualKeywordRecommendationView.as_view(), name='manual_keywords_recommend'),
    path('interests/manual/save/', ManualKeywordSaveView.as_view(), name='manual_keywords_save'),
    path('interests/manual/delete/', DeleteKeywordView.as_view(), name='manual_keywords_delete'),

    # 사용자 저장된 키워드 목록
    path('interests/list/', UserKeywordListView.as_view(), name='user_keywords_list'),
]
