from django.urls import path
from .views import (
    upload_image,
    check_message,               # 기존 send_message → check_message로 명확하게
    get_user_chat_rooms,
    get_chat_room_detail,
    send_message_to_room,
    can_send_message,
)

urlpatterns = [
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('rooms/<int:room_id>/', get_chat_room_detail, name='chat_room_detail'),

    path('message/check/', check_message, name='check_message'),        # ✅ 메시지 필터링 확인용
    path('message/send/', send_message_to_room, name='send_message'),   # ✅ 실제 메시지 저장

    path('upload/image/', upload_image, name='upload_image'),
    path('can_send/', can_send_message, name='can_send_message'),
]
