from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .firebase import upload_file_to_firebase
from .models import Photo

# Create your views here.
class PhotoUploadView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Missing image'}, status=400)
        print(image, image.name)

        public_url = upload_file_to_firebase(image, image.name)
        print(public_url)

        photo = Photo.objects.create(image=image, firebase_url=public_url)
        return Response({'firebase_url' : public_url})

