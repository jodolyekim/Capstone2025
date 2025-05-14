"""
ASGI config for config project.

<<<<<<< HEAD
This config supports both HTTP and WebSocket using Django Channels.
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# ✅ settings 등록 및 Django 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# ✅ routing은 setup 이후에 import
import chat.routing

# ✅ ASGI 애플리케이션 정의
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP 요청 처리
    "websocket": AuthMiddlewareStack(  # WebSocket 요청 처리
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
=======
It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
>>>>>>> feature/alerts-photo-notification
