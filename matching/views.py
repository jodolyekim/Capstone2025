from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from users.models import CustomUser, Profile
from matching.models import Match
from chat.models import ChatRoom  # ChatRoom은 chat.models에서 import해야 합니다
from interest.models import Interest
from photos.models import ProfilePhoto  # ✅ 정확한 모델명
from .utils import haversine, MAPPING


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request):
    user = request.user
    response = request.data.get('response')
    target_user_id = request.data.get('target_user_id')

    if not response or response not in MAPPING:
        return Response({"error": "응답 형식이 잘못되었습니다."}, status=400)

    try:
        other_user = CustomUser.objects.get(id=target_user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "대상 유저를 찾을 수 없습니다."}, status=404)

    user1, user2 = sorted([user, other_user], key=lambda u: u.id)
    match, _ = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        defaults={'status_user1': 'pending', 'status_user2': 'pending', 'matched_keywords': []}
    )

    if user == match.user1:
        match.status_user1 = MAPPING[response]
    else:
        match.status_user2 = MAPPING[response]

    match.save()  # 상태 먼저 저장

    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()

        room, created = ChatRoom.objects.get_or_create(match=match)
        if created:
            room.participants.set([match.user1, match.user2])
            room.save()

    return Response({'message': '응답이 저장되었습니다.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_match(request):
    user = request.user
    target_user_id = request.data.get('target_user_id')

    try:
        target_user = CustomUser.objects.get(id=target_user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': '대상 유저가 존재하지 않습니다.'}, status=404)

    user1, user2 = sorted([user, target_user], key=lambda u: u.id)

    # 여기서 user.profile.interests로 수정
    keywords_user = set(user.profile.interests.values_list('keyword', flat=True))
    keywords_target = set(target_user.profile.interests.values_list('keyword', flat=True))
    matched_keywords = list(keywords_user & keywords_target)

    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        defaults={
            'status_user1': 'accepted' if user == user1 else 'pending',
            'status_user2': 'accepted' if user == user2 else 'pending',
            'matched_keywords': matched_keywords,
        }
    )

    if not created:
        if user == match.user1:
            match.status_user1 = 'accepted'
        else:
            match.status_user2 = 'accepted'

    match.save()  # 상태 저장

    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()

        room, created = ChatRoom.objects.get_or_create(match=match)
        if created:
            room.participants.set([match.user1, match.user2])
            room.save()

    return Response({
        'message': '매칭 응답 완료',
        'match_id': match.id,
        'chat_created': match.is_matched
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_candidates(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return Response({"error": "프로필이 존재하지 않습니다."}, status=400)

    my_lat = profile.current_location_lat
    my_lon = profile.current_location_lon
    my_gender = profile.my_gender
    my_preferred = profile.preferred_gender
    max_distance = profile.match_distance or 5
    my_keywords = set(profile.interests.values_list('keyword', flat=True))

    # 이전 매칭 제외
    past_matches = Match.objects.filter(Q(user1=user) | Q(user2=user))
    exclude_ids = {
        m.user2.id if m.user1 == user else m.user1.id
        for m in past_matches if (m.status_user1 != 'pending' if m.user1 == user else m.status_user2 != 'pending')
    }

    candidates = Profile.objects.exclude(user=user).filter(is_approved=True)
    result = []

    for candidate in candidates:
        candidate_user = candidate.user
        if candidate_user.id in exclude_ids:
            continue

        # ✅ 성별 상호 일치 필터
        # 내가 원하는 성별이 후보자 성별과 일치하는지
        if my_preferred != "모두" and candidate.my_gender != my_preferred:
            continue
        # 후보자가 나를 원하는지
        if candidate.preferred_gender != "모두" and candidate.preferred_gender != my_gender:
            continue

        # ✅ 거리 필터
        if not all([my_lat, my_lon, candidate.current_location_lat, candidate.current_location_lon]):
            continue

        distance = round(haversine(
            my_lat, my_lon,
            candidate.current_location_lat,
            candidate.current_location_lon
        ))
        if distance > max_distance:
            continue

        # ✅ 키워드 필터
        candidate_keywords = set(candidate.interests.values_list('keyword', flat=True))
        common_keywords = list(candidate_keywords & my_keywords)
        if not common_keywords:
            continue

        # ✅ 프로필 사진
        photo_url = None
        if hasattr(candidate, 'photo') and candidate.photo.image:
            photo_url = request.build_absolute_uri(candidate.photo.image.url)

        try:
            match = Match.objects.get(
                Q(user1=user, user2=candidate_user) | Q(user1=candidate_user, user2=user)
            )
            match_id = match.id
        except Match.DoesNotExist:
            match_id = None

        result.append({
            "match_id": match_id,
            "user_id": candidate_user.id,
            "name": candidate.name or "이름 없음",
            "photo": photo_url,
            "distance": distance,
            "keywords": list(candidate_keywords),
            "common_keywords": common_keywords,
            "common_count": len(common_keywords),
        })

    result.sort(key=lambda x: x["common_count"], reverse=True)

    total = len(result)
    for idx, r in enumerate(result):
        r["position"] = f"후보 {idx + 1}/{total}"

    return Response(result)
