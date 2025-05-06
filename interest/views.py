from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .gpt_utils import extract_keywords_by_gpt
from .models import Interest, InterestCategory, InterestKeywordCategoryMap
from users.models import User

import json


class GPTKeywordExtractionView(APIView):
    def post(self, request):
        intro_text = request.data.get("intro_text")
        if not intro_text:
            return Response({"error": "자기소개 텍스트가 필요합니다."}, status=400)

        try:
            result = extract_keywords_by_gpt(intro_text)
            return Response({"result": result}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GPTKeywordSaveView(APIView):
    def post(self, request):
        user = request.user
        intro_text = request.data.get("intro_text")

        if not intro_text:
            return Response({"error": "자기소개 텍스트가 필요합니다."}, status=400)

        try:
            result_str = extract_keywords_by_gpt(intro_text)
            result_json = json.loads(result_str)

            for category_name, keywords in result_json.items():
                category, _ = InterestCategory.objects.get_or_create(name=category_name)

                for keyword in keywords:
                    interest, _ = Interest.objects.get_or_create(
                    user=user,
                    keyword=keyword,
                    defaults={"source": "gpt"}
                )


                    # 중복 연결 방지
                    already_exists = InterestKeywordCategoryMap.objects.filter(
                        user=user,
                        interest=interest,
                        category=category
                    ).exists()

                    if not already_exists:
                        InterestKeywordCategoryMap.objects.create(
                            user=user,
                            interest=interest,
                            category=category
                        )

            return Response({"message": "키워드 저장 완료!"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
