from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ✅ 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, label="비밀번호 확인")

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'blank': '이메일을 입력해주세요.',
                    'invalid': '유효한 이메일 주소를 입력해주세요.',
                    'required': '이메일은 필수 항목입니다.',
                    'unique': '이미 사용 중인 이메일입니다.',
                }
            },
            'password': {
                'write_only': True,
                'error_messages': {
                    'blank': '비밀번호를 입력해주세요.',
                    'required': '비밀번호는 필수 항목입니다.',
                }
            },
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

# ✅ 프로필 시리얼라이저
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

# ✅ 커스텀 JWT 로그인 시리얼라이저

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(
            required=True,
            error_messages={
                'blank': '이메일을 입력해주세요.',
                'required': '이메일을 입력해주세요.',
                'invalid': '유효한 이메일 형식을 입력해주세요.'
            }
        )
        self.fields['password'] = serializers.CharField(
            required=True,
            write_only=True,
            error_messages={
                'blank': '비밀번호를 입력해주세요.',
                'required': '비밀번호를 입력해주세요.',
            }
        )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({
                'password': ['비밀번호가 틀렸습니다.']
            })

        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email
        data['is_profile_set'] = user.is_profile_set
        return data