from django.urls import path
from .views import (
    upload_image,
    send_message,
    get_user_chat_rooms,
    chat_room_list  # ✅ 우리가 새로 추가한 채팅방 목록 view
)

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),
    path('rooms/', chat_room_list, name='chat_room_list'),  # ✅ 여기를 실제로 사용
]
