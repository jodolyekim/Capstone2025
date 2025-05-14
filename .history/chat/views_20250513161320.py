# chat/views.py

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
def send_message(request):
    """
    의심스러운 형식의 메시지만 GPT 필터링을 거쳐 판단하고, 나머지는 통과
    """
    message = request.data.get("message", "").strip()
    msg_type = request.data.get("type", "text")  # ✅ 추가
    if msg_type == "image":                      # ✅ 추가
        return Response({"message": "이미지 전송 허용"}, status=200)  # ✅ 추가

    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    # ✅ 1차 형식 필터링
    suspicious = False
    if re.search(r"\d{3}-\d{3,4}-\d{4}", message):  # 전화번호
        suspicious = True
    elif re.search(r"\d{5,}", message):  # 주민번호/계좌번호 가능
        suspicious = True
    elif any(bad in message.lower() for bad in ["씨발", "좆", "ㅅㅂ", "fuck", "bitch", "꺼져"]):
        suspicious = True
    elif "@" in message and "." in message:  # 이메일 가능성
        suspicious = True

    # ✅ GPT는 의심 메시지에만 판단 요청
    if suspicious:
        try:
            if is_sensitive_message(message):
                return Response({"error": "부적절한 메시지입니다."}, status=403)
        except Exception as e:
            return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)

    return Response({"message": "전송 가능"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    의심스러운 형식의 메시지만 GPT 필터링을 거쳐 판단하고, 나머지는 통과
    """
    message = request.data.get("message", "").strip()
    if not message:
        return Response({"error": "메시지를 입력해주세요."}, status=400)

    # ✅ 1차 형식 필터링
    suspicious = False
    if re.search(r"\d{3}-\d{3,4}-\d{4}", message):  # 전화번호
        suspicious = True
    elif re.search(r"\d{5,}", message):  # 주민번호/계좌번호 가능
        suspicious = True
    elif any(bad in message.lower() for bad in ["씨발", "좆", "ㅅㅂ", "fuck", "bitch", "꺼져"]):
        suspicious = True
    elif "@" in message and "." in message:  # 이메일 가능성
        suspicious = True

    # ✅ GPT는 의심 메시지에만 판단 요청
    if suspicious:
        try:
            if is_sensitive_message(message):
                return Response({"error": "부적절한 메시지입니다."}, status=403)
        except Exception as e:
            return Response({"error": f"GPT 판단 실패: {str(e)}"}, status=500)

    return Response({"message": "전송 가능"})
