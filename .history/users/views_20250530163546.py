from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.db import IntegrityError
from django.core.files.storage import default_storage
from math import radians, sin, cos, asin, sqrt

from .models import CustomUser, Profile, Match, Guardian, ChatRoom
from .serializers import (
    SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer, GuardianSerializer
)
from users.models import Interest, Photo, SuggestedInterest
from users.models import Profile
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)

#인증 및 유저 관련련
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': '중복된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "email": request.user.email,
            "is_profile_set": request.user.is_profile_set
        })

#프로필 관련
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        step = 0
        if all([profile._name, profile._birthYMD, profile._gender, profile._sex_orientation]):
            step = 1
        if profile._communication_way:
            step = 2
        if profile._current_location_lat and profile._current_location_lon and profile._match_distance:
            step = 3
        if all([
            profile._protector_info_name,
            profile._protector_info_birth_date,
            profile._protector_info_phone,
            profile._protector_info_relationship
        ]):
            step = 4
        if user.interests.exists():
            step = 5

        if step == 5 and not user.is_profile_set:
            user.is_profile_set = True
            user.save()

        return Response({"message": "프로필 저장 완료", "profile_step_status": step})
    return Response(serializer.errors, status=400)


class MarkProfileCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        request.user.is_profile_set = True
        request.user.save()
        return Response({'message': '프로필 설정 완료'})

#보호자 관련
class GuardianCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuardianUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            guardian = Guardian.objects.filter(user=request.user).latest('id')
            if 'family_certificate' in request.FILES:
                file = request.FILES['family_certificate']
                path = default_storage.save(f"guardian/family_{request.user.id}_{file.name}", file)
                guardian.family_certificate_url = default_storage.url(path)
            if 'disability_certificate' in request.FILES:
                file = request.FILES['disability_certificate']
                path = default_storage.save(f"guardian/disability_{request.user.id}_{file.name}", file)
                guardian.disability_certificate_url = default_storage.url(path)
            guardian.save()
            return Response({"message": "서류 업로드가 완료되었습니다."})
        except Guardian.DoesNotExist:
            return Response({"error": "보호자 정보가 없습니다."}, status=404)

#매칭 및 채팅방 생성
MAPPING = {
    '승낙': 'accepted',
    '거절': 'rejected',
    'accept': 'accepted',
    'reject': 'rejected',
}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request):
    user = request.user
    response = request.data.get('response')
    target_user_id = request.data.get('target_user_id')

    MAPPING = {
        '승낙': 'accepted',
        '거절': 'rejected',
        'accept': 'accepted',
        'reject': 'rejected',
    }

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
            room.save()  # ✅ 꼭 있어야 DB에 반영됨
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
        room, created = ChatRoom.objects.get_or_create(match=match)
        if created:
            room.participants.set([match.user1, match.user2])
            room.save()  # ✅ participants 반영 위해 반드시 필요

    match.save()
    return Response({
        'message': '매칭 응답 완료',
        'match_id': match.id,
        'chat_created': match.is_matched
    })


#거리 계산 & 후보자 추천
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c


# #관심사 관련
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def save_gpt_interest(request):
#     user = request.user
#     try:
#         data = request.data
#         user.interests.filter(source='gpt').delete()
#         for category, keywords in data.items():
#             for kw in keywords:
#                 if kw.strip():
#                     user.interests.create(keyword=kw.strip(), category=category, source='gpt')
#         return Response({"message": "GPT 키워드가 저장되었습니다."}, status=201)
#     except Exception as e:
#         logger.error(f"❌ GPT 키워드 저장 오류: {e}")
#         return Response({"error": "GPT 키워드 저장 중 오류 발생"}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_manual_interest(request):
    user = request.user
    try:
        keywords = request.data.get("keywords", [])
        if not isinstance(keywords, list):
            return Response({"error": "키워드는 리스트 형태여야 합니다."}, status=400)
        user.interests.filter(source='manual').delete()
        for kw in keywords:
            if kw.strip():
                user.interests.create(keyword=kw.strip(), source="manual")
        return Response({"message": "관심사가 저장되었습니다."}, status=201)
    except Exception as e:
        logger.error(f"❌ 수동 키워드 저장 오류: {e}")
        return Response({"error": "관심사 저장 중 오류 발생"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_manual_interest_keywords(request):
    try:
        user = request.user
        keywords = user.interests.filter(source='manual').values_list('keyword', flat=True)
        return Response({"keywords": list(keywords)})
    except Exception as e:
        return Response({"error": "관심사 조회 오류"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggested_interests(request):
    data = {}
    suggestions = SuggestedInterest.objects.filter(is_active=True).order_by('category__name', 'display_order')
    for item in suggestions:
        cat = item.category.name
        if cat not in data:
            data[cat] = []
        data[cat].append(item.keyword)
    return Response(data)





from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from math import radians, sin, cos, asin, sqrt
from .serializers import (
    SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer, GuardianSerializer
)
from .models import CustomUser, Profile, Match, Guardian, ChatRoom
import logging
from users.models import Interest  # ✅ 관계 모델 명시적으로 import!
from users.models import Photo
from users.models import SuggestedInterest

logger = logging.getLogger(__name__)


# ✅ 회원가입 API
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'error': '중복된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ JWT 로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ✅ 현재 유저 정보
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "email": request.user.email,
            "is_profile_set": request.user.is_profile_set
        })

# ✅ 프로필 조회 및 수정
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

# ✅ 단계별 프로필 저장
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        step = 0
        if all([profile._name, profile._birthYMD, profile._gender, profile._sex_orientation]):
            step = 1
        if profile._communication_way:
            step = 2
        if profile._current_location_lat and profile._current_location_lon and profile._match_distance:
            step = 3
        if all([
            profile._protector_info_name,
            profile._protector_info_birth_date,
            profile._protector_info_phone,
            profile._protector_info_relationship
        ]):
            step = 4
        if user.interests.exists():
            step = 5

        if step == 5 and not user.is_profile_set:
            user.is_profile_set = True
            user.save()

        return Response({
            "message": "프로필 저장 완료",
            "profile_step_status": step
        })

    return Response(serializer.errors, status=400)

# ✅ 최종 완료 시 호출
class MarkProfileCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        request.user.is_profile_set = True
        request.user.save()
        return Response({'message': '프로필 설정 완료'})

# ✅ 보호자 정보 등록
class GuardianCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 보호자 서류 업로드
class GuardianUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            guardian = Guardian.objects.filter(user=request.user).latest('id')

            if 'family_certificate' in request.FILES:
                family_file = request.FILES['family_certificate']
                family_path = default_storage.save(
                    f"guardian/family_{request.user.id}_{family_file.name}", family_file
                )
                guardian.family_certificate_url = default_storage.url(family_path)

            if 'disability_certificate' in request.FILES:
                disability_file = request.FILES['disability_certificate']
                disability_path = default_storage.save(
                    f"guardian/disability_{request.user.id}_{disability_file.name}", disability_file
                )
                guardian.disability_certificate_url = default_storage.url(disability_path)

            guardian.save()
            return Response({"message": "서류 업로드가 완료되었습니다."}, status=200)

        except Guardian.DoesNotExist:
            return Response({"error": "보호자 정보가 없습니다."}, status=404)

# ✅ 수락/거절 처리
MAPPING = {
    '승낙': 'accepted',
    '거절': 'rejected',
    'accept': 'accepted',
    'reject': 'rejected',
}

# ✅ views.py에서
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request):
    print("📩 받은 데이터:", request.data)  # 이거 추가
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
        defaults={
            'status_user1': 'pending',
            'status_user2': 'pending',
            'matched_keywords': [],
        }
    )

    print(f"🔥 Created: {created}, 상태 전: {match.status_user1}, {match.status_user2}")

    if user == match.user1:
        match.status_user1 = MAPPING[response]
    elif user == match.user2:
        match.status_user2 = MAPPING[response]

    # 두 사람이 모두 승낙했는지 확인
    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()

        # 채팅방 생성
        room, created = ChatRoom.objects.get_or_create(match=match)
        if created:
            room.participants.set([match.user1, match.user2])
            print(f"🟢 ChatRoom 생성됨: {room.id}")
    else:
        match.save()
        print(f"🟡 Match 저장됨: {match.id}, 상태: {match.status_user1}, {match.status_user2}")

    return Response({'message': '응답이 저장되었습니다.'})







# ✅ 거리 계산 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

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
    my_match_distance = profile._match_distance or 5  # 기본값 5km

    # 후보자 필터링: 자기 자신 제외, 승인된 유저만
    candidates = Profile.objects.exclude(user=user).filter(is_approved=True)

    result = []
    for candidate in candidates:
        candidate_user = candidate.user
        candidate_keywords = set(candidate_user.interests.values_list('keyword', flat=True))

        # 키워드 1개 이상 겹쳐야 통과
        common_keywords = list(candidate_keywords & my_keywords)
        if not common_keywords:
            continue

        # 거리 필터링
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

        # 성별 및 성적 지향 필터링 (선호 조건이 설정된 경우만 적용)
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



# ✅ GPT 키워드 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_gpt_interest(request):
    user = request.user
    try:
        data = request.data
        print("✅ GPT 응답 데이터:", data)

        # 기존 GPT 관심사 삭제
        user.interests.filter(source='gpt').delete()

        for category, keywords in data.items():
            for kw in keywords:
                if kw.strip():
                    user.interests.create(keyword=kw.strip(), category=category, source='gpt')

        return Response({"message": "GPT 키워드가 저장되었습니다."}, status=201)

    except Exception as e:
        print("❌ GPT 키워드 저장 오류:", e)
        return Response({"error": "GPT 키워드 저장 중 오류가 발생했습니다."}, status=500)


# ✅ 수동 키워드 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_manual_interest(request):
    user = request.user
    try:
        keywords = request.data.get("keywords", [])

        if not isinstance(keywords, list):
            return Response({"error": "키워드는 리스트 형태여야 합니다."}, status=400)

        user.interests.filter(source='manual').delete()

        for kw in keywords:
            if kw.strip():
                user.interests.create(keyword=kw.strip(), source="manual")

        return Response({"message": "관심사가 저장되었습니다."}, status=201)

    except Exception as e:
        print("❌ 수동 키워드 저장 오류:", e)
        return Response({"error": "수동 키워드 저장 중 오류가 발생했습니다."}, status=500)


# ✅ 수동 키워드 조회 (500 방지용)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_manual_interest_keywords(request):
    try:
        user = request.user
        manual_keywords = user.interests.filter(source='manual').values_list('keyword', flat=True)
        return Response({"keywords": list(manual_keywords)})

    except Exception as e:
        print("❌ 수동 키워드 조회 오류:", e)
        return Response({"error": "관심사 조회 중 오류가 발생했습니다."}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggested_interests(request):
    data = {}
    suggestions = SuggestedInterest.objects.filter(is_active=True).order_by('category__name', 'display_order')
    for item in suggestions:
        cat = item.category.name
        if cat not in data:
            data[cat] = []
        data[cat].append(item.keyword)
    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Match, ChatRoom, CustomUser

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

    # 중복 키워드 가져오기
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
