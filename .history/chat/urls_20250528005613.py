from django.urls import path
from .views import upload_image, send_message, get_user_chat_rooms  # ✅ 두 함수 등록

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
]
