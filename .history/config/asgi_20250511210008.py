"""
ASGI config for config project.

This config supports both HTTP and WebSocket using Django Channels.
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat.routing  # ✅ WebSocket 경로 등록용

# Django 설정 로딩
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# ASGI 애플리케이션 정의
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP 요청 처리
    "websocket": AuthMiddlewareStack(  # WebSocket 요청 처리
        URLRouter(
            chat.routing.websocket_urlpatterns  # 채팅 라우팅에서 경로 불러오기
        )
    ),
})
