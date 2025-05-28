from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .gpt_utils import extract_keywords_by_gpt
from .models import Interest, InterestCategory, InterestKeywordCategoryMap
from users.models import CustomUser
from .serializers import InterestSerializer
from django.db.models import Prefetch
import json

class GPTKeywordExtractionView(APIView):
    def post(self, request):
        intro_text = request.data.get("intro_text")
        if not intro_text:
            return Response({"error": "자기소개 텍스트가 필요합니다."}, status=400)

        try:
            print(f"[GPT 요청 텍스트] {intro_text}")  # 입력값 로그
            result = extract_keywords_by_gpt(intro_text)
            return Response({"result": result}, status=200)
        except Exception as e:
            print(f"[GPT 호출 오류] {e}")
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
            print(f"[GPT 저장 오류] {e}")
            return Response({"error": str(e)}, status=500)

class UserKeywordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        interests = Interest.objects.filter(user=user).order_by("-created_at")
        serializer = InterestSerializer(interests, many=True)
        return Response({"keywords": serializer.data}, status=200)

class ManualKeywordRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            data = {}

            category_maps = InterestKeywordCategoryMap.objects.select_related(
                "category", "interest"
            ).filter(user=user).distinct()

            for mapping in category_maps:
                cat_name = mapping.category.name
                keyword = mapping.interest.keyword

                if cat_name not in data:
                    data[cat_name] = set()
                data[cat_name].add(keyword)

            json_ready = {k: list(v) for k, v in data.items()}
            return Response(json_ready, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ManualKeywordSaveView(APIView):
    def post(self, request):
        user = request.user
        data = request.data

        keywords = data.get("keywords")
        category_name = data.get("category")

        if not keywords or not category_name:
            return Response({"error": "카테고리와 키워드가 필요합니다."}, status=400)

        current_count = Interest.objects.filter(user=user).count()
        if current_count >= 10:
            return Response({"error": "최대 10개의 키워드까지만 저장할 수 있습니다."}, status=400)

        category, _ = InterestCategory.objects.get_or_create(name=category_name)
        saved_count = 0

        for keyword in keywords:
            if Interest.objects.filter(user=user, keyword=keyword).exists():
                continue

            if current_count + saved_count >= 10:
                break

            interest = Interest.objects.create(
                user=user,
                keyword=keyword,
                source="manual"
            )

            InterestKeywordCategoryMap.objects.create(
                user=user,
                interest=interest,
                category=category
            )

            saved_count += 1

        return Response({"message": f"{saved_count}개의 키워드를 저장했습니다."}, status=201)

class DeleteKeywordView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        keyword = request.data.get("keyword")
        category_name = request.data.get("category")

        if not keyword or not category_name:
            return Response({"error": "키워드와 카테고리명이 필요합니다."}, status=400)

        try:
            category = InterestCategory.objects.get(name=category_name)
            interest = Interest.objects.filter(user=user, keyword=keyword).first()

            if interest:
                InterestKeywordCategoryMap.objects.filter(
                    user=user, interest=interest, category=category
                ).delete()

                remaining = InterestKeywordCategoryMap.objects.filter(interest=interest)
                if not remaining.exists():
                    interest.delete()

            return Response({"message": "키워드 삭제 완료"}, status=200)

        except InterestCategory.DoesNotExist:
            return Response({"error": "해당 카테고리가 존재하지 않습니다."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
