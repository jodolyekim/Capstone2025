from datetime import timedelta
from django.utils import timezone
from users.models import Guardian

from .sms_mock import send_sms_mock

def notify_guardian_if_needed(user):
    """
    가입 72시간 이내인 사용자가 사진을 전송하면 보호자에게 알림을 보낸다.
    """
    if timezone.now() - user.created_at > timedelta(hours=72):
        return  # 가입한 지 72시간 초과 → 알림 X

    guardians = user.guardians.all()
    if not guardians.exists():
        return  # 보호자 정보 없음

    for guardian in guardians:
        message = f"{user.email} 님이 사진을 전송했습니다. 문제가 있다면 확인해주세요."
        send_sms_mock(guardian.phone, message)
