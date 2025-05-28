import os
import uuid
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.utils.gpt_judge import is_sensitive_message
from chat.utils.message_filtering import detect_message_reason, REASON_MESSAGES
from alerts.utils import notify_guardian_if_needed  # 상단에 추가
from .models import ChatRoom  # ✅ ChatRoom 모델 import


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    이미지 파일을 업로드받아 서버에 저장하고, 접근 가능한 URL을 반환합니다.
    텍스트 설명 없이 이미지 자체만 업로드 가능 (필터링 없음)
    """

    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': '이미지 파일이 없습니다.'}, status=400)

    # 파일명 생성
    extension = image_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # 파일 저장
    with open(filepath, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    # 이미지 URL 생성
    image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")

    # ✅ 보호자 알림 호출
    notify_guardian_if_needed(request.user)

    return Response({'image_url': image_url}, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    의심스러운 형식의 메시지만 GPT 필터링을 거쳐 판단하고,
    차단 시에는 사유와 부드러운 system_message를 함께 전달함.
    """
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")

    # 이미지 메시지는 필터링하지 않음
    if msg_type == "image":
        return Response({"message": "이미지 전송 허용"}, status=200)

    # 비어있는 메시지 예외 처리
    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    # 정규식 기반 사전 필터링
    reason = detect_message_reason(message)

    if reason:
        try:
            # GPT에게 문맥 기반 확인 요청
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_chat_rooms(request):
    """
    현재 로그인된 유저가 포함된 채팅방 목록을 반환합니다.
    participants 필드 기반으로 조회하며, 상대방 정보도 포함합니다.
    """
    user = request.user
    rooms = ChatRoom.objects.filter(participants=user).distinct()

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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatRoom

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room_list(request):
    user = request.user
    print("✅ 현재 로그인 유저:", user.email)  # 🔍 확인용
    rooms = ChatRoom.objects.filter(participants=user)
    print("✅ 참여한 채팅방 수:", rooms.count())
    for r in rooms:
        print(" - ", r.chatroom, [u.email for u in r.participants.all()])

    result = [
        {
            'room_id': room.chatroom,
            'target_user_email': next(
                (u.email for u in room.participants.all() if u != user),
                '알 수 없음'
            )
        }
        for room in rooms
    ]
    return Response(result)
