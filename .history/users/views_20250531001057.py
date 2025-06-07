from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.core.files.storage import default_storage
from django.db import IntegrityError

from .models import CustomUser, Profile, Guardian
from .serializers import (
    SignupSerializer, ProfileSerializer, CustomTokenObtainPairSerializer, GuardianSerializer
)

# ✅ 회원가입
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

    data = request.data.copy()

    # 성적 지향에 따라 preferred_gender 결정
    sex_orientation = data.get("sex_orientation")  # "이성을 만나고 싶어요", ...
    my_gender = data.get("my_gender")              # "남자" or "여자"

    if sex_orientation and my_gender:
        if sex_orientation == "이성을 만나고 싶어요":
            data["preferred_gender"] = "여자" if my_gender == "남자" else "남자"
        elif sex_orientation == "동성을 만나고 싶어요":
            data["preferred_gender"] = my_gender
        elif sex_orientation == "모두 만나고 싶어요":
            data["preferred_gender"] = "모두"

    # 관심사 저장
    interest_ids = data.get("interests")
    if interest_ids:
        profile.interests.set(interest_ids)

    # 필드 저장
    serializer = ProfileSerializer(profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()

        step = 0
        if profile.my_gender and profile.preferred_gender and profile.name and profile.birth_date:
            step = 1
        if profile.communication_way:
            step = 2
        if profile.current_location_lat and profile.current_location_lon and profile.match_distance:
            step = 3
        if all([
            profile.protector_info_name,
            profile.protector_info_birth_date,
            profile.protector_info_phone,
            profile.protector_info_relationship
        ]):
            step = 4

        if step == 4 and not user.is_profile_set:
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
