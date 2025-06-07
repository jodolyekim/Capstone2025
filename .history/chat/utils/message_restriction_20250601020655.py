from datetime import timedelta
from django.utils import timezone
from chat.models import Message

# 송신 제한 여부 판단
def is_sending_restricted(user, chatroom, max_messages=10, recent_minutes=10):
    """
    특정 채팅방에서 사용자의 메시지 송신을 제한해야 하는지 판단한다.
    - 최근 가입자이고
    - 상대방이 답장을 하지 않았으며
    - 10개 연속으로 메시지를 보냈다면 제한

    Args:
        user: 현재 사용자
        chatroom: ChatRoom 인스턴스
        max_messages: 제한 기준 메시지 수 (기본 10)
        recent_minutes: 최근 가입자 기준 시간 (기본 10분, 실제는 72시간 예정)

    Returns:
        (bool, str): 제한 여부와 이유 메시지
    """
    # 1. 최근 가입자인지 확인
    join_delta = timezone.now() - user.date_joined
    if join_delta > timedelta(minutes=recent_minutes):
        return False, ""

    # 2. 최근 메시지 중 이 채팅방에서 보낸 메시지 추적
    recent_messages = Message.objects.filter(chatroom=chatroom).order_by('-created_at')[:max_messages + 10]

    consecutive_count = 0
    for msg in reversed(recent_messages):  # 오래된 순서부터 검사
        if msg.sender == user:
            consecutive_count += 1
        else:
            # 상대방이 한 번이라도 보냈으면 제한 안 함
            return False, ""

    if consecutive_count >= max_messages:
        return True, "상대방의 응답 없이 메시지를 10개 이상 보냈습니다. 잠시 후 다시 시도해주세요."

    return False, ""
