import os
import uuid
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    이미지 파일을 업로드받아 서버에 저장하고, 접근 가능한 URL을 반환합니다.
    """
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': '이미지 파일이 없습니다.'}, status=400)

    # 파일명 랜덤화 (UUID) 후 저장
    extension = image_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # 파일 저장
    with open(filepath, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    # 접근 가능한 URL 반환
    image_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")
    return Response({'image_url': image_url}, status=200)
