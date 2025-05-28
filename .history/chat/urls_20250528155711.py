from django.urls import path
from .views import (
    upload_image,
    send_message,
    get_user_chat_rooms,
    ChatRoomDetailView,
    MessageSendView,
    can_send_message,  # ✅ 이미 import 돼 있음
)

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('room/<int:room_id>/', ChatRoomDetailView.as_view(), name='chat_room_detail'),
    path('message/send/', MessageSendView.as_view(), name='message_send'),
    path('can_send/', can_send_message, name='can_send_message'),  # ✅ 추가됨
]
