import os
import uuid
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.utils.gpt_judge import is_sensitive_message
from chat.utils.message_filtering import detect_message_reason, REASON_MESSAGES
from alerts.utils import notify_guardian_if_needed
from chat.models import ChatRoom, Message

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
def send_message(request):
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")
    room_id = request.data.get("room_id")  # 채팅방 식별자 필요
    user = request.user

    if not room_id:
        return Response({"error": "room_id가 필요합니다."}, status=400)

    # ✅ 가입 72시간 이내 + 상대방 답변 없음 + 메시지 10개 이상이면 제한
    try:
        room = ChatRoom.objects.get(id=room_id)
        messages = room.messages.order_by('sent_at')
        user_messages = messages.filter(sender=user)
        other_messages = messages.exclude(sender=user)

        if (timezone.now() - user.created_at < timedelta(hours=72) and
            user_messages.count() >= 10 and
            other_messages.count() == 0):
            return Response({
                "blocked": True,
                "reason": "상대방의 답장이 없는 상태에서 과도한 메시지를 보내고 있어 채팅이 제한됩니다."
            }, status=403)
    except ChatRoom.DoesNotExist:
        return Response({"error": "채팅방을 찾을 수 없습니다."}, status=404)

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
def report_message(request):
    """
    특정 메시지에 대한 신고를 처리합니다.
    """
    from chat.models import Message, Report
    from chat.serializers import ReportSerializer

    serializer = ReportSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        report = serializer.save()
        return Response({"success": f"메시지 {report.message.id} 신고가 접수되었습니다."}, status=201)
    else:
        return Response(serializer.errors, status=400)
