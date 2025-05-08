from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ✅ 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'required': '이메일을 입력해주세요.',
                    'invalid': '올바른 이메일 형식이 아닙니다.',
                    'unique': '이미 사용 중인 이메일입니다.',
                }
            },
            'password': {
                'write_only': True,
                'error_messages': {
                    'required': '비밀번호를 입력해주세요.',
                }
            },
            'password2': {
                'error_messages': {
                    'required': '비밀번호 확인을 입력해주세요.',
                }
            }
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
            '_name',
            '_birthYMD',
            '_gender',
            '_sex_orientation',
            '_communication_way',
            '_current_location_lat',
            '_current_location_lon',
            '_match_distance',
            '_protector_info_name',
            '_protector_info_birth_date',
            '_protector_info_phone',
            '_protector_info_relationship',
        ]
        read_only_fields = ['user']
        extra_kwargs = {
            '_name': {'required': False, 'allow_blank': True},
            '_birthYMD': {'required': False},
            '_gender': {'required': False, 'allow_blank': True},
            '_sex_orientation': {'required': False, 'allow_blank': True},
            '_communication_way': {'required': False},
            '_current_location_lat': {'required': False},
            '_current_location_lon': {'required': False},
            '_match_distance': {'required': False},
            '_protector_info_name': {'required': False, 'allow_blank': True},
            '_protector_info_birth_date': {'required': False},
            '_protector_info_phone': {'required': False, 'allow_blank': True},
            '_protector_info_relationship': {'required': False, 'allow_blank': True},
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
                raise serializers.ValidationError(
                    {"detail": "이메일 또는 비밀번호가 올바르지 않습니다."}
                )
        else:
            raise serializers.ValidationError(
                {"detail": "이메일과 비밀번호를 모두 입력해주세요."}
            )

        data = super().validate(attrs)
        data["user_id"] = user.id
        data["email"] = user.email
        data["is_profile_set"] = user.is_profile_set
        return data
