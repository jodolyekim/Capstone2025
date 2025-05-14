from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'created_at']
    search_fields = ['chatroom']
    list_filter = ['created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'sender', 'input_msg', 'created_at']
    search_fields = ['sender__email', 'input_msg']
    list_filter = ['chatroom', 'created_at']
