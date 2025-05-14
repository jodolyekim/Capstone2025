# chat/urls.py

from django.urls import path
from .views import upload_image, send_message  # ✅ send_message 추가

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),  # ✅ GPT 필터링용 전송 API 추가
]
