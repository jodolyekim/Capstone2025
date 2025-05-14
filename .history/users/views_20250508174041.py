from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes

from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser

# ✅ 회원가입 처리
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer


# ✅ JWT 로그인 처리 (email 기반)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': '이미 존재하는 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ 프로필 조회 및 수정 (Flutter에서 GET / PATCH 요청 처리)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# ✅ 현재 로그인한 사용자 정보 조회 (Flutter 로그인 상태 확인용)
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


# ✅ Flutter 프로필 설정 각 단계에서 부분 업데이트 처리
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_partial(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
