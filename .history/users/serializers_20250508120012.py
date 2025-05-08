from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ✅ 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

# ✅ 프로필 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id']

# ✅ 커스텀 JWT 로그인 시리얼라이저 (이메일 기반)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD  # email로 로그인

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # ✅ username=email 로 넘겨야 백엔드가 인식 가능
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.", code='authorization')
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해주세요.", code='authorization')

        data = super().validate(attrs)
        data["user_id"] = user.id
        data["username"] = user.username
        data["is_profile_set"] = user.is_profile_set
        return data
