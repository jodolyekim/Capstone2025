from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile, Guardian
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ✅ 회원가입용 시리얼라이저
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
        extra_kwargs = {f: {'required': False, 'allow_blank': True} for f in fields if f != 'user'}

# ✅ JWT 커스텀 로그인 시리얼라이저
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

        # ✅ 단계별 상태 계산
        try:
            profile = user.profile
            step = 0
            if all([profile._name, profile._birthYMD, profile._gender, profile._sex_orientation]):
                step = 1
            if profile._communication_way:
                step = 2
            if profile._current_location_lat and profile._current_location_lon and profile._match_distance:
                step = 3
            if all([profile._protector_info_name, profile._protector_info_birth_date,
                    profile._protector_info_phone, profile._protector_info_relationship]):
                step = 4
            if user.interests.exists():
                step = 5
        except Profile.DoesNotExist:
            step = 0

        data['profile_step_status'] = step  # 🔥 클라이언트에 전달

        return data

# ✅ 보호자 정보 시리얼라이저
class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = ['id', 'name', 'phone', 'relation', 'is_visible',
                  'family_certificate_url', 'disability_certificate_url']
