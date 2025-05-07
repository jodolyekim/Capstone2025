from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .firebase import upload_file_to_firebase
from .models import Photo
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
class PhotoUploadView(APIView):
    def post(self, request):
        image: InMemoryUploadedFile = request.FILES['image']
        public_url = upload_file_to_firebase(image, image.name)
        photo = Photo.objects.create(image=image, firebase_url=public_url)
        return Response({'firebase_url' : public_url})