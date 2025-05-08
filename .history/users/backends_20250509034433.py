from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser

# 이메일을 아이디로 사용하는 사용자 인증 백엔드 정의
class EmailBackend(ModelBackend):
    # username 대신 email을 사용해 로그인 처리
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 이메일로 사용자 조회
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            # 존재하지 않으면 None 반환
            return None

        # 비밀번호 일치 시 사용자 반환
        if user.check_password(password):
            return user

        # 비밀번호 불일치 시 인증 실패
        return None
