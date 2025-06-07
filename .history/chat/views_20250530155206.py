import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer
from chat.utils.gpt_judge import is_sensitive_message
from chat.utils.message_filtering import detect_message_reason, REASON_MESSAGES
from alerts.utils import notify_guardian_if_needed
from users.models import CustomUser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_chat_rooms(request):
    user = request.user
    print("🔎 현재 유저:", user.id, user.email)

    rooms = ChatRoom.objects.filter(participants=user).distinct()
    print("✅ 찾은 방 수:", rooms.count())
    for room in rooms:
        print("🧩 방 ID:", room.id, "참여자 수:", room.participants.count())
        for p in room.participants.all():
            print("    ↪", p.id, p.email)

    result = []
    for room in rooms:
        others = room.participants.exclude(id=user.id)
        target_user = others.first() if others.exists() else None

        result.append({
            "room_id": room.id,
            "other_user_email": target_user.email if target_user else "상대 없음",
            "other_user_name": target_user.profile._name if target_user and hasattr(target_user, 'profile') else "이름 없음"
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

    match = room.match
    other_user = match.user1 if match.user2 == user else match.user2

    return Response({
        "room_id": room.id,
        "match_id": match.id,
        "other_user_email": other_user.email,
        "other_user_name": other_user.profile._name or "이름 없음"
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
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

    return Response({"message": "전송 가능"}, status=200)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_to_room(request):
    room_id = request.data.get('chatroom')
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)

    message = Message.objects.create(
        chatroom=room,
        sender=request.user,
        input_msg=request.data.get('input_msg', ''),
        msg_type=request.data.get('msg_type', 'text'),
    )
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def can_send_message(request):
    user = request.user
    can_send = hasattr(user, 'profile') and getattr(user.profile, 'is_verified', True)
    return Response({'can_send': can_send})
