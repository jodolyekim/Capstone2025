from django.urls import path
from .views import (
    upload_image,
    send_message,
    get_user_chat_rooms,
    get_chat_room_detail,
    send_message_to_room,
    can_send_message,
)

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('send/', send_message, name='send_message'),
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('rooms/<int:room_id>/', get_chat_room_detail, name='chat_room_detail'),
    path('message/send/', send_message_to_room, name='message_send'),
    path('can_send/', can_send_message, name='can_send_message'),
]
