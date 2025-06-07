from django.urls import path
from .views import (
    GPTKeywordExtractionView,
    GPTKeywordSaveView,
    UserKeywordListView,
    ManualKeywordView,
    DeleteKeywordView,
)

urlpatterns = [
    # ✅ GPT 키워드 추출
    path('keywords/extract/', GPTKeywordExtractionView.as_view()),       # 공식 경로
    path('gpt/',           GPTKeywordExtractionView.as_view()),       # 예전 Flutter 요청 대응

    # ✅ GPT 키워드 저장
    path('keywords/save/', GPTKeywordSaveView.as_view()),                # 공식 경로
    path('save/',          GPTKeywordSaveView.as_view()),                # 예전 Flutter 요청 대응

    # ✅ 내 키워드 조회
    path('keywords/',      UserKeywordListView.as_view()),

    # ✅ 수동 키워드 조회/저장 (GET=추천, POST=저장)
    path('keywords/manual/', ManualKeywordView.as_view()),
    path('keywords/manual/recommend/', ManualKeywordView.as_view()),    # 공식 경로 GET 대응
    path('suggestions/',   ManualKeywordView.as_view()),                # 예전 Flutter GET 요청 대응

    # ✅ 키워드 삭제
    path('keywords/delete/', DeleteKeywordView.as_view()),
]
