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
    path("gpt/", GPTKeywordExtractionView.as_view()),                      # ✅ Flutter용 경로 추가
    path("extract-keywords/", GPTKeywordExtractionView.as_view()),        # 기존 경로 유지해도 OK
    path("save-keywords/", GPTKeywordSaveView.as_view()),
    path("my-keywords/", UserKeywordListView.as_view()),
    path("manual-keywords/", ManualKeywordRecommendationView.as_view()),
    path("save-manual-keywords/", ManualKeywordSaveView.as_view()),
    path("delete-keyword/", DeleteKeywordView.as_view()),
]
