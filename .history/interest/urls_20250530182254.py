urlpatterns = [
    # ✅ GPT 키워드 추출 (정식 경로 + 예전 호환 경로)
    path("keywords/extract/", GPTKeywordExtractionView.as_view()),      
    path("gpt/", GPTKeywordExtractionView.as_view()),                   # ← 예전 Flutter 요청 대응

    # ✅ GPT 키워드 저장
    path("keywords/save/", GPTKeywordSaveView.as_view()),
    path("save/", GPTKeywordSaveView.as_view()),                        # ← 예전 Flutter 요청 대응

    # ✅ 내 키워드 조회
    path("keywords/", UserKeywordListView.as_view()),                   

    # ✅ 수동 키워드 저장
    path("keywords/manual/", ManualKeywordSaveView.as_view()),          

    # ✅ 수동 추천 키워드 조회
    path("keywords/manual/recommend/", ManualKeywordRecommendationView.as_view()),  
    path("suggestions/", ManualKeywordRecommendationView.as_view()),   # ← 예전 Flutter 요청 대응

    # ✅ 키워드 삭제
    path("keywords/delete/", DeleteKeywordView.as_view()),              
]
