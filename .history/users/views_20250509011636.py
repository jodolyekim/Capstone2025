from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from django.utils import timezone

from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser, Profile

# ✅ 회원가입 처리 (토큰 발급 포함)
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

        except IntegrityError as e:
            msg = str(e).lower()
            if 'email' in msg:
                return Response({'error': '이미 사용 중인 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in msg:
                return Response({'error': '이미 사용 중인 사용자 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': '중복된 값이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ JWT 로그인 처리 (email 기반)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ✅ 프로필 전체 조회/수정
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# ✅ 현재 로그인한 사용자 정보
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

# ✅ Flutter 프로필 설정 각 단계별 저장 (POST 방식)
@api_view(['PATCH'])  # PATCH 요청을 허용하도록 수정
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        # 모든 주요 필드가 채워졌으면 is_profile_set = True
        required_keys = [
            'name', 'birth_date', 'gender', 'sexual_orientation',
            'communication_styles', 'latitude', 'longitude', 'match_distance_km'
        ]
        if all(getattr(profile, key, None) for key in required_keys):
            user.is_profile_set = True
            user.save()

        return Response({"message": "Profile step saved successfully."}, status=200)

    return Response(serializer.errors, status=400)
