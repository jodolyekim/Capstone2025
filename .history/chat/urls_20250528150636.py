from django.urls import path
from .views import (
    upload_image,
    send_message,
    get_user_chat_rooms,
    ChatRoomDetailView,
    MessageSendView,
)

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('room/<int:room_id>/', ChatRoomDetailView.as_view(), name='chat_room_detail'),
    path('message/send/', MessageSendView.as_view(), name='message_send'),
]
