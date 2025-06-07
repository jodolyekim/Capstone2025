from django.urls import path
from .views import (
    GPTKeywordExtractionView,
    GPTKeywordSaveView,
    UserKeywordListView,
    ManualKeywordRecommendationView,
    ManualKeywordSaveView,
    DeleteKeywordView,
)

urlpatterns = [
    path("keywords/extract/", GPTKeywordExtractionView.as_view()),      # GPT 키워드 추출
    path("keywords/save/", GPTKeywordSaveView.as_view()),               # GPT 키워드 저장
    path("keywords/", UserKeywordListView.as_view()),                   # 내 키워드 조회
    path("keywords/manual/", ManualKeywordSaveView.as_view()),          # 수동 키워드 저장
    path("keywords/manual/recommend/", ManualKeywordRecommendationView.as_view()),  # 수동 추천 키워드 조회
    path("keywords/delete/", DeleteKeywordView.as_view()),              # 키워드 삭제
]
