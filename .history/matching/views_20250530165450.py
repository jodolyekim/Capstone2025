from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from users.models import CustomUser, Match, ChatRoom, Profile
from .utils import haversine
from .constants import MAPPING

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
    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        defaults={'status_user1': 'pending', 'status_user2': 'pending', 'matched_keywords': []}
    )

    if user == match.user1:
        match.status_user1 = MAPPING[response]
    elif user == match.user2:
        match.status_user2 = MAPPING[response]

    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()
        room, created = ChatRoom.objects.get_or_create(match=match)
        if created:
            room.participants.set([match.user1, match.user2])
            room.save()
    else:
        match.save()

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
    keywords_user = set(user.interests.values_list('keyword', flat=True))
    keywords_target = set(target_user.interests.values_list('keyword', flat=True))
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

    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        ChatRoom.objects.get_or_create(match=match)

    match.save()
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

    my_lat = profile._current_location_lat
    my_lon = profile._current_location_lon
    my_keywords = set(user.interests.values_list('keyword', flat=True))
    my_preferred_gender = profile.preferred_gender
    my_preferred_orientation = profile.preferred_orientation
    my_match_distance = profile._match_distance or 5

    candidates = Profile.objects.exclude(user=user).filter(is_approved=True)

    result = []
    for candidate in candidates:
        candidate_user = candidate.user
        candidate_keywords = set(candidate_user.interests.values_list('keyword', flat=True))
        common_keywords = list(candidate_keywords & my_keywords)
        if not common_keywords:
            continue

        if all([my_lat, my_lon, candidate._current_location_lat, candidate._current_location_lon]):
            distance = round(haversine(
                my_lat, my_lon,
                candidate._current_location_lat,
                candidate._current_location_lon
            ))
            if distance > my_match_distance:
                continue
        else:
            distance = "알 수 없음"

        if my_preferred_gender and candidate._gender and my_preferred_gender != candidate._gender:
            continue
        if my_preferred_orientation and candidate._sex_orientation and my_preferred_orientation != candidate._sex_orientation:
            continue

        try:
            photo_url = request.build_absolute_uri(candidate.photo.image.url)
        except:
            photo_url = None

        try:
            match = Match.objects.get(user1__in=[user, candidate_user], user2__in=[user, candidate_user])
            match_id = match.id
        except Match.DoesNotExist:
            match_id = None

        result.append({
            "match_id": match_id,
            "user_id": candidate_user.id,
            "name": candidate._name or "이름 없음",
            "photo": photo_url,
            "distance": distance,
            "keywords": list(candidate_keywords),
            "common_keywords": common_keywords,
        })

    return Response(result)
