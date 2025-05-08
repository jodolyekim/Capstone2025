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

# ✅ 회원가입 처리 (중복 이메일 예외 처리 포함 + 토큰 발급 포함)
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            user = CustomUser.objects.get(email=request.data['email'])

            # 토큰 발급
            refresh = RefreshToken.for_user(user)
            response.data['access'] = str(refresh.access_token)

            return response
        except IntegrityError as e:
            print("🔥 IntegrityError 발생:", e)
            msg = str(e).lower()
            if 'email' in msg:
                return Response({'error': '이미 사용 중인 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in msg:
                return Response({'error': '이미 사용 중인 사용자 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': '중복된 값이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ JWT 로그인 처리 (email 기반)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ✅ 프로필 조회 및 수정
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# ✅ 현재 로그인한 사용자 정보 조회
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

# ✅ Flutter 프로필 설정 각 단계에서 부분 업데이트
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_partial(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'name': '',
            'birth_date': timezone.now().date(),
            'gender': '미정',
            'sexual_orientation': '미정',
            'communication_styles': [],
            'latitude': 0.0,
            'longitude': 0.0,
            'match_distance_km': 5,
        }
    )
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        user.is_profile_set = True
        user.save()
        return Response({"message": "Profile updated successfully."}, status=200)
    return Response(serializer.errors, status=400)
