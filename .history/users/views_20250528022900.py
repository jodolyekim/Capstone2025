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

# ✅ 매칭 수락/거절 처리
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request, match_id):
    action = request.data.get("action")  # "accept" 또는 "reject"
    current_user = request.user

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "매칭이 존재하지 않습니다."}, status=404)

    if current_user not in [match.user1, match.user2]:
        return Response({"error": "이 매칭에 대한 권한이 없습니다."}, status=403)

    # 현재 유저 기준으로 수락/거절 상태 저장
    if current_user == match.user1:
        match.status_user1 = 'accepted' if action == 'accept' else 'rejected'
    else:
        match.status_user2 = 'accepted' if action == 'accept' else 'rejected'

    # 둘 다 수락한 경우
    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()

        if not hasattr(match, 'chatroom'):
            ChatRoom.objects.create(match=match)

        return Response({
            "message": "상대방도 당신에게 승낙을 이미 눌렀습니다. 채팅방이 생성되었습니다.",
            "match_id": match.id,
            "chat_created": True
        })

    # 한쪽이라도 거절한 경우
    match.save()
    return Response({
        "message": f"매칭이 {action} 처리되었습니다.",
        "match_id": match.id,
        "chat_created": False
    })

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
    current_user = request.user
    try:
        my_profile = current_user.profile
    except Profile.DoesNotExist:
        return Response({"error": "프로필이 존재하지 않습니다."}, status=400)

    my_lat = my_profile._current_location_lat
    my_lon = my_profile._current_location_lon
    my_keywords = set(current_user.interests.values_list('keyword', flat=True))

    # 거절된 상대는 제외
    candidates = Profile.objects.exclude(user=current_user).filter(is_approved=True).exclude(
        user__matches_as_user1__user2=current_user,
        user__matches_as_user1__status_user1='rejected'
    ).exclude(
        user__matches_as_user2__user1=current_user,
        user__matches_as_user2__status_user2='rejected'
    )

    result = []
    for profile in candidates:
        candidate_user = profile.user
        candidate_keywords = set(candidate_user.interests.values_list('keyword', flat=True))
        common_keywords = list(candidate_keywords & my_keywords)

        try:
            photo_obj = profile.photo
            photo_url = request.build_absolute_uri(photo_obj.image.url)
        except Photo.DoesNotExist:
            photo_url = None

        distance = "알 수 없음"
        if my_lat and my_lon and profile._current_location_lat and profile._current_location_lon:
            distance = round(haversine(
                my_lat, my_lon,
                profile._current_location_lat,
                profile._current_location_lon
            ))

        result.append({
            "match_id": candidate_user.id,
            "name": profile._name or "이름 없음",
            "photo": photo_url,
            "distance": distance,
            "keywords": list(candidate_keywords),
            "common_keywords": common_keywords,
        })

    return Response(result)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_manual_interest(request):
    keywords = request.data.get("keywords", [])
    user = request.user

    # 기존 관심사 삭제
    user.interests.all().delete()

    # 새 관심사 저장
    for kw in keywords:
        if kw.strip():
            user.interests.create(keyword=kw.strip(), source="manual")

    return Response({"message": "관심사가 저장되었습니다."}, status=201)

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