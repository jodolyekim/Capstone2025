from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .gpt_utils import extract_keywords_by_gpt
from users.models import (
    Interest,
    InterestCategory,
    InterestKeywordCategoryMap,
    CustomUser
)
from .serializers import InterestSerializer

class GPTKeywordExtractionView(APIView):
    def post(self, request):
        intro_text = request.data.get("intro_text")
        if not intro_text:
            return JsonResponse({"error": "자기소개 텍스트가 필요합니다."}, status=400, json_dumps_params={'ensure_ascii': False})

        try:
            result = extract_keywords_by_gpt(intro_text)
            return JsonResponse({"result": result}, status=200, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, json_dumps_params={'ensure_ascii': False})


class GPTKeywordSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        intro_text = request.data.get("intro_text")

        if not intro_text:
            return JsonResponse({"error": "자기소개 텍스트가 필요합니다."}, status=400, json_dumps_params={'ensure_ascii': False})

        try:
            result_json = extract_keywords_by_gpt(intro_text)

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

            user.is_profile_set = True
            user.save()

            return JsonResponse({"message": "GPT 키워드 저장 완료. 프로필이 완료되었습니다."}, status=201, json_dumps_params={'ensure_ascii': False})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, json_dumps_params={'ensure_ascii': False})


class UserKeywordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        interests = Interest.objects.filter(user=user).order_by("-id")
        serializer = InterestSerializer(interests, many=True)
        return JsonResponse({"keywords": serializer.data}, status=200, safe=False, json_dumps_params={'ensure_ascii': False})


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
            return JsonResponse(json_ready, status=200, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, json_dumps_params={'ensure_ascii': False})


class ManualKeywordSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        keywords = data.get("keywords")
        category_name = data.get("category")

        if not keywords or not category_name:
            return JsonResponse({"error": "카테고리와 키워드가 필요합니다."}, status=400, json_dumps_params={'ensure_ascii': False})

        current_count = Interest.objects.filter(user=user).count()
        if current_count >= 10:
            return JsonResponse({"error": "최대 10개의 키워드까지만 저장할 수 있습니다."}, status=400, json_dumps_params={'ensure_ascii': False})

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

        user.is_profile_set = True
        user.save()

        return JsonResponse({"message": f"{saved_count}개의 키워드를 저장했습니다. 프로필이 완료되었습니다."}, status=201, json_dumps_params={'ensure_ascii': False})


class DeleteKeywordView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        keyword = request.data.get("keyword")
        category_name = request.data.get("category")

        if not keyword or not category_name:
            return JsonResponse({"error": "키워드와 카테고리명이 필요합니다."}, status=400, json_dumps_params={'ensure_ascii': False})

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

            return JsonResponse({"message": "키워드 삭제 완료"}, status=200, json_dumps_params={'ensure_ascii': False})

        except InterestCategory.DoesNotExist:
            return JsonResponse({"error": "해당 카테고리가 존재하지 않습니다."}, status=404, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, json_dumps_params={'ensure_ascii': False})
