from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import Profile, Match
from users.serializers import ProfileSerializer
from matching.matching import is_mutually_acceptable, has_common_keywords
from django.db.models import Q

class MatchingCandidatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            my_profile = user.profile
        except Profile.DoesNotExist:
            return Response({"error": "프로필 정보가 없습니다."}, status=400)

        my_keywords = set(user.interests.values_list('keyword', flat=True))

        # ✅ 후보군: 자기 자신 제외 + 활성 유저
        candidates = Profile.objects.exclude(user=user).filter(user__is_active=True)

        # ✅ 이미 수락/거절한 사람 or 나를 거절한 사람 제외
        decided_matches = Match.objects.filter(
            Q(user1=user, status_user1__in=['accepted', 'rejected']) |
            Q(user2=user, status_user2__in=['accepted', 'rejected']) |
            Q(user1__ne=user, status_user2='rejected') |  # 나를 거절한 상대
            Q(user2__ne=user, status_user1='rejected')
        ).values_list('user1', 'user2')

        # 튜플(flatten) -> ID set으로
        exclude_ids = set()
        for u1, u2 in decided_matches:
            exclude_ids.add(u1)
            exclude_ids.add(u2)
        exclude_ids.discard(user.id)

        candidates = candidates.exclude(user__id__in=exclude_ids)

        # ✅ 성향 + 키워드 겹침 필터링
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
