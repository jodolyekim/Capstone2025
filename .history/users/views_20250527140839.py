from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from django.utils import timezone

from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model

from .serializers import SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer, GuardianSerializer
from .models import CustomUser, Profile, Match, Guardian, ChatRoom

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

# JWT 로그인 커스텀 뷰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 프로필 CRUD
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# 로그인한 사용자 정보 확인
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

# 프로필 각 단계 저장 (is_profile_set 설정 X)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile step saved successfully."}, status=200)
    return Response(serializer.errors, status=400)

# ✅ 관심사 입력 완료 후 계정 활성화 처리 API
class MarkProfileCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        user.is_profile_set = True
        user.save()
        return Response({"message": "프로필 설정이 완료되었습니다."}, status=200)

# 매칭 수락/거절
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_match(request, match_id):
    action = request.data.get("action")
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "매칭이 존재하지 않습니다."}, status=404)

    current_user = request.user
    if current_user not in [match.user1, match.user2]:
        return Response({"error": "이 매칭에 대한 권한이 없습니다."}, status=403)

    if current_user == match.user1:
        match.status_user1 = 'accepted' if action == 'accept' else 'rejected'
    else:
        match.status_user2 = 'accepted' if action == 'accept' else 'rejected'

    if match.status_user1 == 'accepted' and match.status_user2 == 'accepted':
        match.is_matched = True
        match.matched_at = timezone.now()
        match.save()
        if not hasattr(match, 'chatroom'):
            ChatRoom.objects.create(match=match)
    else:
        match.save()

    return Response({"message": f"매칭이 {action} 처리되었습니다."})

# Firebase 로그인 연동
User = get_user_model()

class FirebaseLoginView(APIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        if not id_token:
            return Response({"error": "idToken이 누락되었습니다."}, status=400)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email', f'{uid}@firebase.local')

            user, created = User.objects.get_or_create(username=uid, defaults={'email': email})
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
            })

        except Exception as e:
            return Response({"error": f"Firebase 인증 실패: {str(e)}"}, status=401)

# 보호자 정보 입력
class GuardianCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 보호자 서류 업로드
class GuardianUploadView(APIView):
    def post(self, request):
        return Response({"message": "업로드 성공"})
