from datetime import timedelta
from django.utils import timezone
from chat.models import Message

# 🚫 송신 제한 여부 판단
def is_sending_restricted(user, chatroom, max_messages=10, recent_days=3):
    """
    특정 채팅방에서 사용자의 메시지 송신을 제한해야 하는지 판단한다.

    Args:
        user: 현재 사용자
        chatroom: ChatRoom 인스턴스
        max_messages: 제한 기준 메시지 수 (기본: 10)
        recent_days: 신규 사용자 기준 기간 (기본: 3일)

    Returns:
        (bool, str): 제한 여부와 제한 이유 메시지
    """
    # 1. 가입 기간 확인 (3일 이내 가입자만 제한 대상)
    join_delta = timezone.now() - user.date_joined
    if join_delta.days > recent_days:
        return False, ""

    # 2. 해당 채팅방의 최근 메시지 가져오기
    recent_messages = Message.objects.filter(chatroom=chatroom).order_by('-created_at')[:max_messages + 10]

    # 3. 사용자 메시지만 필터링 (연속 카운트용)
    consecutive_user_msgs = 0
    for msg in reversed(recent_messages):  # 오래된 메시지부터
        if msg.sender == user:
            consecutive_user_msgs += 1
        else:
            # 상대방이 한 번이라도 답장하면 제한 안 걸림
            return False, ""

    # 4. 답장이 아예 없고, 연속 메시지가 10개 이상인 경우 제한
    if consecutive_user_msgs >= max_messages:
        return True, "상대방의 응답이 없는데 메시지를 10개 이상 보냈습니다. 잠시 후 다시 시도해주세요."

    return False, ""
