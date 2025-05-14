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

# ✅ 프로필 시리얼라이저 (명시적 필드 지정 + optional 필드 대응)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'name',
            'birth_date',
            'gender',
            'sexual_orientation',
            'communication_styles',
            'latitude',
            'longitude',
            'match_distance_km',
            'guardian_name',
            'guardian_birth_date',
            'guardian_phone',
            'guardian_relationship',
        ]
        read_only_fields = ['user']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'birth_date': {'required': False},
            'gender': {'required': False, 'allow_blank': True},
            'sexual_orientation': {'required': False, 'allow_blank': True},
            'communication_styles': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'match_distance_km': {'required': False},
            'guardian_name': {'required': False, 'allow_blank': True},
            'guardian_birth_date': {'required': False},
            'guardian_phone': {'required': False, 'allow_blank': True},
            'guardian_relationship': {'required': False, 'allow_blank': True},
        }

# ✅ 커스텀 JWT 로그인 시리얼라이저 (이메일 기반)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
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
