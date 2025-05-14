from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser


# ✅ 회원가입 처리
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer


# ✅ JWT 로그인 처리 (email 기반)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ✅ 프로필 조회 및 수정
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  # ✅ signals로 생성된 Profile 객체에 안전하게 접근


# ✅ 현재 로그인한 사용자 정보 조회 (Flutter 로그인 후 상태 확인용)
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
