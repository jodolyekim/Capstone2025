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


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from users.models import Profile, Guardian
from users.serializers import ProfileSerializer, GuardianSerializer
from interest.models import Interest


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def save_or_update_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    data = request.data.copy()
    print("📩 받은 데이터:", data)

    # ✅ 필드 매핑
    field_map = {
        "_name": "name",
        "_birthYMD": "birth_date",
        "_gender": "my_gender",
        "_sex_orientation": "sex_orientation",
        "_communication_way": "communication_way",
        "_current_location_lat": "current_location_lat",
        "_current_location_lon": "current_location_lon",
        "_match_distance": "match_distance",
        "_interests": "interests",
          # ✅ 보호자 필드 추가
        "_protector_name": "protector_info_name",
        "_protector_birth": "protector_info_birth_date",
        "_protector_phone": "protector_info_phone",
        "_protector_relationship": "protector_info_relationship",
    }

    for old_key, new_key in field_map.items():
        if old_key in data:
            data[new_key] = data.pop(old_key)

    # ✅ gender 변환 처리
    gender_map = {"남성": "남자", "여성": "여자"}
    if "my_gender" in data and data["my_gender"] in gender_map:
        data["my_gender"] = gender_map[data["my_gender"]]

    # ✅ preferred_gender 자동 설정
    sex_orientation = data.get("sex_orientation")
    my_gender = data.get("my_gender")

    if sex_orientation and my_gender:
        if sex_orientation == "이성을 만나고 싶어요":
            data["preferred_gender"] = "여자" if my_gender == "남자" else "남자"
        elif sex_orientation == "동성을 만나고 싶어요":
            data["preferred_gender"] = my_gender
        elif sex_orientation == "모두 만나고 싶어요":
            data["preferred_gender"] = "모두"

    # ✅ 관심사 설정 (문자열 키워드 기반)
    interest_keywords = data.get("interests")
    if interest_keywords:
        interests = Interest.objects.filter(keyword__in=interest_keywords)
        profile.interests.set(interests)
        print("✅ 관심사 설정 완료:", list(interests.values_list("keyword", flat=True)))

    # ✅ 나머지 저장
    serializer = ProfileSerializer(profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print("✅ 프로필 저장 완료:", serializer.data)

        step = 0
        if all([profile.my_gender, profile.preferred_gender, profile.name, profile.birth_date]):
            step = max(step, 1)
        if profile.communication_way:
            step = max(step, 2)
        if all([profile.current_location_lat, profile.current_location_lon, profile.match_distance]):
            step = max(step, 3)
        if all([
            profile.protector_info_name,
            profile.protector_info_birth_date,
            profile.protector_info_phone,
            profile.protector_info_relationship
        ]):
            step = max(step, 4)

        if step == 4 and not user.is_profile_set:
            user.is_profile_set = True
            user.save()

        return Response({
            "message": "프로필 저장 완료",
            "profile_step_status": step
        })
    else:
        print("❌ serializer.is_valid() 실패")
        print("🚨 오류 내용:", serializer.errors)
        return Response(serializer.errors, status=400)


class MarkProfileCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        request.user.is_profile_set = True
        request.user.save()
        return Response({'message': '프로필 설정 완료'})


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
