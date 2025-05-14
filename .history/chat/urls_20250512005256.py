from django.urls import path
from .views import upload_image  # 이미지 업로드 뷰 임포트

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
]
