# chat/routing.py

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # ✅ UUID 대응 정규식으로 수정
    re_path(r'^ws/chat/(?P<chatroom>[0-9a-f-]+)/$', ChatConsumer.as_asgi()),
]
