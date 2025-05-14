import os
import uuid
import re
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.utils.gpt_judge import is_sensitive_message

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

    extension = image_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")
    return Response({'image_url': image_url}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    의심스러운 형식의 메시지만 GPT 필터링을 거쳐 판단하고, 나머지는 통과
    """
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")
    if msg_type == "image":
        return Response({"message": "이미지 전송 허용"}, status=200)

    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    suspicious = False
    if re.search(r"\d{3}-\d{3,4}-\d{4}", message):
        suspicious = True
    elif re.search(r"\d{5,}", message):
        suspicious = True
    elif any(bad in message.lower() for bad in ["씨발", "좆", "ㅅㅂ", "fuck", "bitch", "꺼져"]):
        suspicious = True
    elif "@" in message and "." in message:
        suspicious = True

    if suspicious:
        try:
            if is_sensitive_message(message):
                return Response({"error": "부적절한 메시지입니다."}, status=403)
        except Exception as e:
            return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)

    return Response({"message": "전송 가능"})
