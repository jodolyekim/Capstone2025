# matching/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import Profile
from users.serializers import ProfileSerializer
from users.models import Interest
from matching.matching import is_mutually_acceptable, has_common_keywords

class MatchingCandidatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            my_profile = user.profile
        except Profile.DoesNotExist:
            return Response({"error": "프로필 정보가 없습니다."}, status=400)

        my_keywords = set(user.interests.values_list('keyword', flat=True))
        candidates = Profile.objects.exclude(user=user).filter(user__is_active=True)

        result = []
        for profile in candidates:
            if not is_mutually_acceptable(my_profile, profile):
                continue

            candidate_keywords = set(profile.user.interests.values_list('keyword', flat=True))
            if not has_common_keywords(my_keywords, candidate_keywords):
                continue

            result.append(profile)

        serializer = ProfileSerializer(result, many=True)
        return Response(serializer.data)
