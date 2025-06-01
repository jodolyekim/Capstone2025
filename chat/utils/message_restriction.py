from datetime import timedelta
from django.utils import timezone
from chat.models import Message

def is_sending_restricted(user, chatroom, max_messages=10, recent_minutes=120):
    """
    최근 가입자가 같은 채팅방에서 10회 이상 연속 메시지를 보냈는지 검사하여 제재 여부 반환.

    조건:
    ① 가입 후 2시간 이내 + 상대방 응답 없이 10개 이상 보냄 → 차단
    ② 상대방이 응답했어도, 그 이후 10개 연속 보냄 → 차단
    """
    now = timezone.now()
    is_recent_joiner = (now - user.date_joined) < timedelta(minutes=recent_minutes)

    print("\n🔍 [제한 검사 시작]")
    print(f"📨 유저: {user.email}")
    print(f"⏱️ 가입 시각: {user.date_joined}")
    print(f"⏱️ 현재 시각: {now}")
    print(f"🕑 가입 {recent_minutes}분 이내? {is_recent_joiner}")

    # ✅ 최근 메시지 (가입 이후만 고려)
    recent_messages = Message.objects.filter(
        chatroom=chatroom,
        created_at__gte=user.date_joined
    ).order_by('-created_at')[:max_messages + 10]

    print(f"📦 최근 메시지 수 (가입 이후): {recent_messages.count()}")

    # ✅ 상대방 정보 및 마지막 응답 확인
    other_user = chatroom.participants.exclude(id=user.id).first()
    last_other_reply = (
        Message.objects.filter(
            chatroom=chatroom,
            sender=other_user,
            created_at__gte=user.date_joined
        ).order_by('-created_at').first()
    )

    print(f"👥 상대방: {other_user.email if other_user else '없음'}")
    print(f"💬 상대방 마지막 응답: {last_other_reply.created_at if last_other_reply else '없음'}")

    # 🚫 조건 ①: 상대방이 응답한 적 없고, 10개 연속으로 보냈는지 확인
    if not last_other_reply:
        consecutive_count = 0
        for msg in reversed(recent_messages):  # 오래된 순서부터 확인
            if msg.sender == user:
                consecutive_count += 1
            else:
                break

        print(f"📊 상대 응답 전 내 연속 메시지 수: {consecutive_count}")
        if consecutive_count >= max_messages:
            print("🚫 제한 조건 ① 충족: 상대 응답 없음 + 10개 이상 전송")
            return True, "상대방이 응답하지 않았는데 메시지를 10개 이상 보냈습니다. 잠시 후 다시 시도해주세요."

        return False, ""

    # 🚫 조건 ②: 상대방이 응답한 이후, 내가 연속으로 10개 이상 보냈는지
    if is_recent_joiner:
        after_reply_msgs = Message.objects.filter(
            chatroom=chatroom,
            created_at__gt=last_other_reply.created_at,
            created_at__gte=user.date_joined
        ).order_by('created_at')

        print(f"📬 상대 응답 이후 메시지 수: {after_reply_msgs.count()}")

        consecutive_after_reply = 0
        for msg in after_reply_msgs:
            if msg.sender == user:
                consecutive_after_reply += 1
                if consecutive_after_reply >= max_messages:
                    print("🚫 제한 조건 ② 충족: 응답 이후 10개 연속 전송")
                    return True, "상대방 응답 이후에도 10개 이상 연속으로 보냈습니다. 제한됩니다."
            else:
                consecutive_after_reply = 0

    print("✅ 제한 조건 미충족: 메시지 전송 허용")
    return False, ""
