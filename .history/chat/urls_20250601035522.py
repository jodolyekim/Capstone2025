from django.urls import path
from .views import (
    upload_image,
    check_message,
    get_user_chat_rooms,
    get_chat_room_detail,
    send_message_to_room,
    can_send_message,
    report_chat,
    get_chat_messages,
    get_chatroom_uuid,
)

urlpatterns = [
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('rooms/<uuid:room_id>/', get_chat_room_detail, name='chat_room_detail'),
    path('rooms/<uuid:room_id>/messages/', get_chat_messages, name='chat_messages'),

    path('message/check/', check_message, name='check_message'),
    path('message/send/', send_message_to_room, name='send_message'),  # ✅ 이게 너가 404 난 부분

    path('upload/image/', upload_image, name='upload_image'),
    path('can_send_message/', can_send_message, name='can_send_message'),

    path('report/', report_chat, name='report_chat'),
    path('get_chatroom_uuid/', get_chatroom_uuid, name='get_chatroom_uuid'),  # ✅ 중복 경로 수정됨
]
