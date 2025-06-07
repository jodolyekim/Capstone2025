from django.urls import path
from .views import (
    upload_image,
    check_message,
    get_user_chat_rooms,
    get_chat_room_detail,
    send_message_to_room,
    can_send_message,
    report_chat,  # ✅ 신고 뷰 추가
    get_chat_messages,  # ✅ 추가
    

)
from chat.views import get_chatroom_uuid
from . import views

urlpatterns = [
    path('rooms/', get_user_chat_rooms, name='chat_rooms'),
    path('rooms/<int:room_id>/', get_chat_room_detail, name='chat_room_detail'),

    path('message/check/', check_message, name='check_message'),        # ✅ 메시지 필터링 확인용
    path('message/send/', send_message_to_room, name='send_message'),   # ✅ 실제 메시지 저장

    path('upload/image/', upload_image, name='upload_image'),
    path('can_send_message/', can_send_message, name='can_send_message'),

    path('report/', report_chat, name='report_chat'),
    path('rooms/<int:room_id>/messages/', get_chat_messages, name='chat_messages'),  # ✅ 추가
    # ✅ 신고 제출 API
    path('api/chat/get_chatroom_uuid/', get_chatroom_uuid),
    path('rooms/<uuid:room_id>/messages/', views.get_chat_messages_by_uuid, name='get_chat_messages_by_uuid'),

]
