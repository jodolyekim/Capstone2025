from django.urls import path
from .views import upload_profile_photo

urlpatterns = [
    path('upload-image/', upload_profile_photo, name='upload-profile-photo'),
]
