from datetime import timedelta
from django.utils import timezone
from chat.models import Message

def is_sending_restricted(user, chatroom, max_messages=10, recent_minutes=120):
    """
    특정 채팅방에서 사용자의 송신 제한 여부 판단.
    최근 가입자(예: 2시간 이내)가 같은 채팅방에서 10회 이상 연속 메시지를 보냈는지 검사.
    """
    now = timezone.now()
    is_recent_joiner = (now - user.date_joined) < timedelta(minutes=recent_minutes)

    # 최근 메시지 중, 가입 이후의 것만 가져오기
    recent_messages = Message.objects.filter(
        chatroom=chatroom,
        created_at__gte=user.date_joined
    ).order_by('-created_at')[:max_messages + 10]

    # 가장 최근 상대방 메시지 확인
    other_user = chatroom.participants.exclude(id=user.id).first()
    last_other_reply = (
        Message.objects.filter(
            chatroom=chatroom,
            sender=other_user,
            created_at__gte=user.date_joined  # 가입 이후의 응답만 고려
        ).order_by('-created_at').first()
    )

    # ① 상대방이 한 번도 답장 안 했을 경우 → 제한 조건 바로 검사
    if not last_other_reply:
        consecutive_count = 0
        for msg in reversed(recent_messages):  # 오래된 순서부터 검사
            if msg.sender == user:
                consecutive_count += 1
            else:
                break
        if consecutive_count >= max_messages:
            return True, "상대방이 응답하지 않았는데 메시지를 10개 이상 보냈습니다. 잠시 후 다시 시도해주세요."

        return False, ""

    # ② 상대방이 응답한 적은 있음 → 그 이후 10개 연속 보냈는지 확인
    if is_recent_joiner:
        after_reply_msgs = Message.objects.filter(
            chatroom=chatroom,
            created_at__gt=last_other_reply.created_at,
            created_at__gte=user.date_joined
        ).order_by('created_at')

        consecutive_after_reply = 0
        for msg in after_reply_msgs:
            if msg.sender == user:
                consecutive_after_reply += 1
                if consecutive_after_reply >= max_messages:
                    return True, "상대방 응답 이후에도 10개 이상 연속으로 보냈습니다. 제한됩니다."
            else:
                consecutive_after_reply = 0

    return False, ""
