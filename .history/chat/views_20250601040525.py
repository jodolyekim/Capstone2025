import os
import uuid
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer
from chat.utils.gpt_judge import is_sensitive_message
from chat.utils.message_filtering import detect_message_reason, REASON_MESSAGES
from sms.utils import notify_guardian_if_needed
from chat.models import ChatReport  # 모델 임포트 필요
from matching.models import Match
from rest_framework import status
from chat.utils.message_restriction import is_sending_restricted  # ✅ 추가


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_chat_rooms(request):
    user = request.user
    rooms = ChatRoom.objects.filter(participants=user).distinct()

    result = []
    for room in rooms:
        others = room.participants.exclude(id=user.id)
        target_user = others.first() if others.exists() else None

        result.append({
            "room_id": room.id,
            "chatroom": str(room.chatroom),  # ✅ WebSocket 연결용 UUID 추가!
            "other_user_email": target_user.email if target_user else "상대 없음",
            "other_user_name": getattr(getattr(target_user, 'profile', None), '_name', '이름 없음')
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_detail(request, room_id):
    user = request.user
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방이 존재하지 않습니다."}, status=404)

    if user not in room.participants.all():
        return Response({"error": "이 채팅방에 접근할 수 없습니다."}, status=403)

    match = getattr(room, 'match', None)
    if not match:
        return Response({"error": "이 채팅방에 연결된 매칭 정보가 없습니다."}, status=400)

    other_user = match.user1 if match.user2 == user else match.user2

    return Response({
        "room_id": room.id,
        "match_id": match.id,
        "other_user_email": other_user.email,
        "other_user_name": getattr(getattr(other_user, 'profile', None), '_name', '이름 없음')
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_message(request):
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")

    if msg_type == "image":
        return Response({"message": "이미지 전송 허용"}, status=200)

    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    reason = detect_message_reason(message)

    if reason:
        try:
            if is_sensitive_message(message):
                system_msg = REASON_MESSAGES.get(reason, REASON_MESSAGES["기타"])
                return Response({
                    "blocked": True,
                    "reason": reason,
                    "system_message": system_msg
                }, status=200)
        except Exception as e:
            return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)

    return Response({"blocked": False, "message": "전송 가능"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_to_room(request):
    room_id = request.data.get('chatroom')
    if not room_id:
        return Response({"error": "채팅방 ID가 없습니다."}, status=400)

    try:
        room = ChatRoom.objects.get(chatroom=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방을 찾을 수 없습니다."}, status=404)

    if request.user not in room.participants.all():
        return Response({"error": "해당 채팅방에 접근 권한이 없습니다."}, status=403)

    if room.participants.count() != 2:
        return Response({"error": "이 채팅방의 참여자 수가 유효하지 않습니다."}, status=400)

    input_msg_raw = request.data.get('input_msg', '')
    input_msg = input_msg_raw.strip() if isinstance(input_msg_raw, str) else ''
    msg_type = request.data.get('msg_type', 'text')

    if msg_type == "text":
        if not input_msg:
            return Response({"error": "빈 메시지는 보낼 수 없습니다."}, status=400)

        # ✅ 송신 제한 검사 (3일 이내 가입자 + 연속 10개 이상 메시지)
        is_restricted, restriction_msg = is_sending_restricted(request.user, room)
        if is_restricted:
            return Response({
                "blocked": True,
                "reason": "초기 가입자 메시지 제한",
                "system_message": restriction_msg
            }, status=200)

        # ✅ 필터링 검사
        reason = detect_message_reason(input_msg)
        if reason:
            try:
                if is_sensitive_message(input_msg):
                    system_msg = REASON_MESSAGES.get(reason, REASON_MESSAGES["기타"])
                    return Response({
                        "blocked": True,
                        "reason": reason,
                        "system_message": system_msg
                    }, status=200)
            except Exception as e:
                return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)
    else:
        reason = ""

    # ✅ 메시지 저장
    message = Message.objects.create(
        chatroom=room,
        sender=request.user,
        input_msg=input_msg,
        msg_type=msg_type,
        format_filtered=bool(reason),
        gpt_filtered=False,
        filtered_msg=input_msg,
        reason=reason or ""
    )

    # ✅ 이미지 전송 시 보호자에게 문자 알림 + 로그 기록
    if msg_type == "image":
        from sms.utils import notify_guardian_if_needed
        event_type = "사진 전송" if request.user == message.sender else "사진 수신"
        notify_guardian_if_needed(request.user, event_type=event_type, message=message)

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=201)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': '이미지 파일이 없습니다.'}, status=400)

    extension = image_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")
    notify_guardian_if_needed(request.user)

    return Response({'image_url': image_url}, status=200)


@api_view(['GET', 'POST'])  # ← 여기에 POST 추가
@permission_classes([IsAuthenticated])
def can_send_message(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    is_approved = getattr(profile, 'is_approved', False)
    return Response({'can_send': is_approved})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_chat(request):
    user = request.user
    room_id = request.data.get('room_id')
    reason = request.data.get('reason')
    custom_reason = request.data.get('custom_reason', '')

    # 채팅방 조회
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방이 존재하지 않습니다."}, status=404)

    if user not in room.participants.all():
        return Response({"error": "이 채팅방에 접근할 수 없습니다."}, status=403)

    # ✅ 중복 신고 방지 (ID로 비교!)
    if ChatReport.objects.filter(reporter=user, chat_room__id=room_id).exists():
        return Response({"error": "이미 이 채팅방을 신고하셨습니다."}, status=400)

    # 대상 사용자 찾기
    target_user = room.participants.exclude(id=user.id).first()

    # 최근 메시지 로그 추출 (20개)
    messages = Message.objects.filter(chatroom=room).order_by('-created_at')[:20]
    log_text = "\n".join([
        f"[{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {m.sender.email}: {m.input_msg or '(사진)'}"
        for m in reversed(messages)
    ])

    # 신고 객체 생성
    ChatReport.objects.create(
        reporter=user,
        reported=target_user,
        chat_room=room,
        reason=reason,
        custom_reason=custom_reason if reason == "other" else "",
        message_snapshot=log_text
    )

    return Response({"message": "신고가 접수되었습니다. 운영팀이 확인 후 조치를 취할 예정입니다."}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, room_id):
    user = request.user
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방이 존재하지 않습니다."}, status=404)

    if user not in room.participants.all():
        return Response({"error": "이 채팅방에 접근할 수 없습니다."}, status=403)

    messages = Message.objects.filter(chatroom=room).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_chatroom_uuid(request):
    match_id = request.data.get("match_id")
    if not match_id:
        return Response({"error": "match_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "매칭 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    try:
        room = ChatRoom.objects.get(match=match)
        return Response({"chatroom": str(room.chatroom)}, status=200)
    except ChatRoom.DoesNotExist:
        return Response({"error": "해당 매칭에 대한 채팅방이 존재하지 않습니다."}, status=404)

# ✅ UUID를 사용하는 메시지 조회 함수
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages_by_uuid(request, room_id):
    user = request.user
    try:
        room = ChatRoom.objects.get(chatroom=room_id)  # UUID 기반 조회
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방이 존재하지 않습니다."}, status=404)

    if user not in room.participants.all():
        return Response({"error": "이 채팅방에 접근할 수 없습니다."}, status=403)

    messages = Message.objects.filter(chatroom=room).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)
