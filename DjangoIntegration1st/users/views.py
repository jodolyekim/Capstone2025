from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError

from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser, Profile, Match

# 회원가입 API 뷰
# - 사용자 생성 후 JWT 토큰 발급
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # 토큰 발급
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            msg = str(e).lower()
            if 'email' in msg:
                return Response({'error': '이미 사용 중인 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in msg:
                return Response({'error': '이미 사용 중인 사용자 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': '중복된 값이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

# 로그인 API 뷰 (JWT 발급)
# - 이메일과 비밀번호 기반
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 프로필 조회/수정 API
# - 로그인된 사용자의 프로필을 가져오거나 수정
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# 현재 로그인한 사용자 정보 조회 API
# - 로그인 상태 확인이나 사용자 정보 가져올 때 사용
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_profile_set": user.is_profile_set
        })

# Flutter 앱에서 단계별 프로필 설정 저장 API
# - 각 스텝마다 PATCH 요청으로 업데이트됨
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        # 주요 필드가 모두 채워졌을 경우, is_profile_set 플래그 설정
        required_keys = [
            '_name', '_birthYMD', '_gender', '_sex_orientation',
            '_communication_way', '_current_location_lat', '_current_location_lon', '_match_distance'
        ]
        if all(getattr(profile, key, None) for key in required_keys):
            user.is_profile_set = True
            user.save()

        return Response({"message": "Profile step saved successfully."}, status=200)

    return Response(serializer.errors, status=400)

# 매칭 수락/거절 처리 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request, match_id):
    action = request.data.get("action")  # "accept" 또는 "reject"
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "매칭이 존재하지 않습니다."}, status=404)

    current_user = request.user
    if current_user not in [match.user1, match.user2]:
        return Response({"error": "이 매칭에 대한 권한이 없습니다."}, status=403)

    # 유저 상태 갱신
    if current_user == match.user1:
        match.status_user1 = 'accepted' if action == 'accept' else 'rejected'
    else:
        match.status_user2 = 'accepted' if action == 'accept' else 'rejected'

    # 양쪽 모두 수락한 경우
    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()
        # 채팅방 생성 (한 번만 생성되도록)
        if not hasattr(match, 'chatroom'):
            ChatRoom.objects.create(match=match)
    else:
        match.save()

    return Response({"message": f"매칭이 {action} 처리되었습니다."})

