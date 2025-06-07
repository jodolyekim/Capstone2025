from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .gpt_utils import extract_keywords_by_gpt
from interest.models import (
    Interest,
    InterestCategory,
    InterestKeywordCategoryMap,
    SuggestedInterest,  # 수동 추천 키워드 모델 추가
)
from users.models import CustomUser
from .serializers import InterestSerializer


class GPTKeywordExtractionView(APIView):
    def post(self, request):
        intro_text = request.data.get("intro_text")
        if not intro_text:
            return JsonResponse(
                {"error": "자기소개 텍스트가 필요합니다."},
                status=400,
                json_dumps_params={'ensure_ascii': False},
            )

        try:
            result = extract_keywords_by_gpt(intro_text)
            return JsonResponse(
                {"result": result},
                status=200,
                json_dumps_params={'ensure_ascii': False},
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500,
                json_dumps_params={'ensure_ascii': False},
            )


class GPTKeywordSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        intro_text = request.data.get("intro_text")

        if not intro_text:
            return JsonResponse(
                {"error": "자기소개 텍스트가 필요합니다."},
                status=400,
                json_dumps_params={'ensure_ascii': False},
            )

        try:
            result_json = extract_keywords_by_gpt(intro_text)

            for category_name, keywords in result_json.items():
                category, _ = InterestCategory.objects.get_or_create(name=category_name)

                for keyword in keywords:
                    interest, _ = Interest.objects.get_or_create(
                        user=user,
                        keyword=keyword,
                        defaults={"source": "gpt"},
                    )

                    already_exists = InterestKeywordCategoryMap.objects.filter(
                        user=user,
                        interest=interest,
                        category=category,
                    ).exists()

                    if not already_exists:
                        InterestKeywordCategoryMap.objects.create(
                            user=user,
                            interest=interest,
                            category=category,
                        )

            user.is_profile_set = True
            user.save()

            return JsonResponse(
                {"message": "GPT 키워드 저장 완료. 프로필이 완료되었습니다."},
                status=201,
                json_dumps_params={'ensure_ascii': False},
            )

        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500,
                json_dumps_params={'ensure_ascii': False},
            )


class UserKeywordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        interests = Interest.objects.filter(user=user).order_by("-id")
        serializer = InterestSerializer(interests, many=True)
        return JsonResponse(
            {"keywords": serializer.data},
            status=200,
            json_dumps_params={'ensure_ascii': False},
        )


class ManualKeywordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        추천 키워드 목록 조회
        """
        try:
            suggestions = (
                SuggestedInterest.objects
                .filter(is_active=True)
                .order_by("display_order")
            )
            data = {}

            for item in suggestions:
                cat_name = item.category.name
                data.setdefault(cat_name, []).append(item.keyword)

            return JsonResponse(
                data,
                status=200,
                json_dumps_params={'ensure_ascii': False},
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500,
                json_dumps_params={'ensure_ascii': False},
            )

    def post(self, request):
        """
        사용자가 선택한 키워드 저장
        """
        user = request.user
        data = request.data

        keywords = data.get("keywords")
        category_name = data.get("category")

        if not keywords or not category_name:
            return JsonResponse(
                {"error": "카테고리와 키워드가 필요합니다."},
                status=400,
                json_dumps_params={'ensure_ascii': False},
            )

        current_count = Interest.objects.filter(user=user).count()
        if current_count >= 10:
            return JsonResponse(
                {"error": "최대 10개의 키워드까지만 저장할 수 있습니다."},
                status=400,
                json_dumps_params={'ensure_ascii': False},
            )

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
                source="manual",
            )
            InterestKeywordCategoryMap.objects.create(
                user=user,
                interest=interest,
                category=category,
            )
            saved_count += 1

        user.is_profile_set = True
        user.save()

        return JsonResponse(
            {"message": f"{saved_count}개의 키워드를 저장했습니다. 총 {len(keywords)}개 중 {len(keywords) - saved_count}개는 제한으로 인해 저장되지 않았습니다."},
            status=201,
            json_dumps_params={'ensure_ascii': False},
        )


class DeleteKeywordView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        keyword = request.query_params.get("keyword")
        category_name = request.query_params.get("category")

        if not keyword or not category_name:
            return JsonResponse(
                {"error": "키워드와 카테고리명이 필요합니다."},
                status=400,
                json_dumps_params={'ensure_ascii': False},
            )

        try:
            category = InterestCategory.objects.get(name=category_name)
            interest = Interest.objects.filter(user=user, keyword=keyword).first()

            if interest:
                InterestKeywordCategoryMap.objects.filter(
                    user=user,
                    interest=interest,
                    category=category,
                ).delete()

                # 매핑이 모두 삭제된 경우, Interest 객체도 삭제
                if not InterestKeywordCategoryMap.objects.filter(interest=interest).exists():
                    interest.delete()

            return JsonResponse(
                {"message": "키워드 삭제 완료"},
                status=200,
                json_dumps_params={'ensure_ascii': False},
            )
        except InterestCategory.DoesNotExist:
            return JsonResponse(
                {"error": "해당 카테고리가 존재하지 않습니다."},
                status=404,
                json_dumps_params={'ensure_ascii': False},
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500,
                json_dumps_params={'ensure_ascii': False},
            )