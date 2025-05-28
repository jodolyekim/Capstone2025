from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
class PhotoUploadView(APIView):
    def post(self, request):
        print("hihi")
        image: InMemoryUploadedFile = request.FILES['image']
        print(image, image.name)

        public_url = upload_file_to_firebase(image, image.name)
        print(public_url)

        photo = Photo.objects.create(image=image, firebase_url=public_url)
        return Response({'firebase_url' : public_url})