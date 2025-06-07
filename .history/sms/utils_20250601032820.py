import logging
from users.models import Guardian
from .sms_real import send_sms_real  # ✅ 실제 문자 전송 함수로 교체
from sms.models import GuardianAlertLog
from chat.models import Message

logger = logging.getLogger(__name__)

def notify_guardian_if_needed(user, event_type="사진 전송", message: Message = None):
    """
    사용자가 사진을 전송하거나 수신하면 보호자에게 문자 알림을 보낸다.
    Args:
        user (CustomUser): 현재 유저 인스턴스
        event_type (str): '사진 전송' 또는 '사진 수신'
        message (Message, optional): 알림과 연결된 채팅 메시지 객체
    """

    guardians = user.guardians.all()
    if not guardians.exists():
        logger.warning(f"⚠️ {user.email} 보호자 정보 없음 → 문자 발송 생략")
        return

    for guardian in guardians:
        if not guardian.phone:
            logger.warning(f"⚠️ 보호자 {guardian.name} 전화번호 없음 → 생략")
            continue

        message_text = f"{user.email} 님이 채팅 중 {event_type}을 했습니다. 문제가 있다면 확인해주세요."

        try:
            logger.info(f"📲 보호자 문자 전송: {guardian.phone} / 내용: {message_text}")
            send_sms_real(guardian.phone, message_text)  # ✅ 실제 문자 전송

            # ✅ 문자 전송 로그 DB에 저장
            if message:
                GuardianAlertLog.objects.create(
                    guardian=guardian,
                    user=user,
                    message=message,
                    event_type=event_type,
                    phone=guardian.phone
                )

        except Exception as e:
            logger.error(f"❌ 문자 전송 실패 ({guardian.phone}): {str(e)}")
