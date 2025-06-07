# chat/routing.py

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # ✅ 채팅방 고유 ID를 URL로 받아 WebSocket 연결
    re_path(r'^ws/chat/(?P<chatroom>\w+)/$', ChatConsumer.as_asgi()),
]
