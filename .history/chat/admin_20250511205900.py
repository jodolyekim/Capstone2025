from django.contrib import admin
from .chat_models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'sender', 'input_msg', 'created_at']
