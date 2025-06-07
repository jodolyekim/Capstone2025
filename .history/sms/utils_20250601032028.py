import logging
from users.models import Guardian
from .sms_mock import send_sms_mock  # 실제 운영 시 sms_real.py로 변경 가능

logger = logging.getLogger(__name__)

def notify_guardian_if_needed(user, event_type="사진 전송"):
    """
    사용자가 사진을 전송하거나 수신하면 보호자에게 문자 알림을 보낸다.
    가입일과 관계없이 항상 실행된다.

    Args:
        user (CustomUser): 현재 유저 인스턴스
        event_type (str): '사진 전송' 또는 '사진 수신'
    """

    guardians = user.guardians.all()
    if not guardians.exists():
        logger.warning(f"⚠️ {user.email} 보호자 정보 없음 → 문자 발송 생략")
        return

    for guardian in guardians:
        if not guardian.phone:
            logger.warning(f"⚠️ 보호자 {guardian.name} 전화번호 없음 → 생략")
            continue

        message = f"{user.email} 님이 채팅 중 {event_type}을 했습니다. 문제가 있다면 확인해주세요."
        try:
            logger.info(f"📲 보호자 문자 전송: {guardian.phone} / 내용: {message}")
            send_sms_mock(guardian.phone, message)
        except Exception as e:
            logger.error(f"❌ 문자 전송 실패 ({guardian.phone}): {str(e)}")
