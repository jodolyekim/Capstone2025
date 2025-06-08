from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProfilePhoto
from users.models import Profile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return Response({'error': '프로필이 존재하지 않습니다.'}, status=404)

    image = request.FILES.get('image')
    if not image:
        return Response({'error': '이미지 파일이 없습니다.'}, status=400)

    # ❌ 기존 사진 제거 X
    profile_photo = ProfilePhoto.objects.create(profile=profile, image=image)

    return Response({'image_url': profile_photo.image.url})
