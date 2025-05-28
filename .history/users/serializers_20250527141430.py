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

        # 🔽 프로필 단계별 완료 여부 판단
        try:
            profile = user.profile
            next_step = 0

            if profile._name and profile._birthYMD and profile._gender and profile._sex_orientation:
                next_step = 1
            if profile._communication_way and len(profile._communication_way) > 0:
                next_step = 2
            if profile._current_location_lat and profile._current_location_lon and profile._match_distance:
                next_step = 3
            if profile._protector_info_name and profile._protector_info_phone and profile._protector_info_relationship:
                next_step = 4

            # 관심사까지 설정된 상태는 백엔드에서는 판단 어려우니 프론트에서 따로 저장
            data['profile_step_status'] = next_step  # ✅ 0~4까지 판단됨

        except Exception:
            data['profile_step_status'] = 0

        return data
