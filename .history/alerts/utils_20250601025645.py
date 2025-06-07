from users.models import Guardian
from .sms_mock import send_sms_mock  # 실제 사용 시 send_sms_real로 교체

def notify_guardian_if_needed(user):
    """
    사용자가 사진을 전송하면 보호자에게 문자 알림을 보낸다.
    가입 시간과 관계없이 항상 실행된다.
    """
    guardians = user.guardians.all()
    if not guardians.exists():
        print("⚠️ 보호자 정보 없음 → 문자 발송 생략")
        return

    for guardian in guardians:
        message = f"{user.email} 님이 사진을 전송했습니다. 문제가 있다면 확인해주세요."
        print(f"📲 보호자 문자 전송: {guardian.phone} / 내용: {message}")
        send_sms_mock(guardian.phone, message)  # ← 필요시 실제 문자 API로 변경
