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
    의심스러운 형식의 메시지만 GPT 필터링을 거쳐 판단하고,
    차단 시에는 사유와 부드러운 system_message를 함께 전달함.
    """
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")
    if msg_type == "image":
        return Response({"message": "이미지 전송 허용"}, status=200)

    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    # 차단 사유 매핑
    REASON_MESSAGES = {
        "욕설": "⚠️ 부드러운 대화를 위해 욕설은 피해주세요.",
        "전화번호": "📞 전화번호처럼 보이는 정보는 공유할 수 없어요.",
        "숫자열": "🔢 너무 긴 숫자는 민감한 정보일 수 있어요.",
        "이메일": "📧 이메일 주소는 이곳에서 공유할 수 없어요.",
        "URL": "🔗 외부 링크는 안전을 위해 전송할 수 없어요.",
        "기타": "❗️이 문장은 조금 위험할 수 있어요. 다른 말로 표현해볼까요?",
    }

    # 형식 필터링
    reason = None
    if re.search(r"https?://\S+", message):
        reason = "URL"
    elif re.search(r"\d{3}-\d{3,4}-\d{4}", message):
        reason = "전화번호"
    elif re.search(r"\d{12,}", message):
        reason = "숫자열"  # 카드번호 등
    elif any(bad in message.lower() for bad in ["씨발", "좆", "ㅅㅂ", "fuck", "bitch", "꺼져"]):
        reason = "욕설"
    elif "@" in message and "." in message:
        reason = "이메일"

    if reason:
        try:
            if is_sensitive_message(message):
                return Response({
                    "blocked": True,
                    "reason": reason,
                    "system_message": REASON_MESSAGES.get(reason, REASON_MESSAGES["기타"])
                }, status=200)
        except Exception as e:
            return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)

    return Response({"message": "전송 가능"}, status=200)
