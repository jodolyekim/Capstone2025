from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError
from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser, Profile, Guardian

# 회원가입 API 뷰
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

# 로그인 API 뷰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 프로필 조회/수정 API
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# 현재 로그인한 사용자 정보 조회 API
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
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        required_keys = [
            '_name', '_birthYMD', '_gender', '_sex_orientation',
            '_communication_way', '_current_location_lat', '_current_location_lon', '_match_distance'
        ]
        if all(getattr(profile, key, None) for key in required_keys):
            user.is_profile_set = True
            user.save()

        return Response({"message": "Profile step saved successfully."}, status=200)

    return Response(serializer.errors, status=400)

# 보호자 서류 업로드 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_guardian_documents(request):
    user = request.user
    try:
        guardian = Guardian.objects.get(user=user)

        if 'family_certificate' in request.FILES:
            guardian.family_certificate = request.FILES['family_certificate']
        if 'disability_certificate' in request.FILES:
            guardian.disability_certificate = request.FILES['disability_certificate']

        guardian.save()

        return Response({'message': '파일 업로드가 완료되었습니다.'}, status=200)
    except Guardian.DoesNotExist:
        return Response({'error': '보호자 정보가 먼저 입력되어야 합니다.'}, status=400)

# 보호자 기본 정보 등록 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_guardian_info(request):
    user = request.user
    data = request.data

    try:
        guardian, created = Guardian.objects.get_or_create(user=user)

        guardian.name = data.get('name', '')
        guardian.phone = data.get('phone', '')
        guardian.relation = data.get('relation', '')
        guardian.save()

        return Response({'message': '보호자 정보가 저장되었습니다.'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
