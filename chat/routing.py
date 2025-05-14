# chat/routing.py

from django.urls import re_path
from . import consumers  # consumers.py에서 WebSocket 로직 처리 예정

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chatroom>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
