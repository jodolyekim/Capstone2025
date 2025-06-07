from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
class PhotoUploadView(APIView):
    def post(self, request):
        print("📷 이미지 업로드 요청 들어옴")
        image: InMemoryUploadedFile = request.FILES['image']
        print(f"파일 이름: {image.name}")

        # Firebase 제거 → 로컬 저장만 수행
        photo = Photo.objects.create(image=image)
        image_url = photo.image.url  # MEDIA_URL + 경로

        return Response({'image_url': image_url})
