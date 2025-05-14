from django.contrib import admin
from .models import ChatRoom, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'input_msg', 'created_at')
    can_delete = False

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'created_at']
    search_fields = ['chatroom']
    list_filter = ['created_at']
    inlines = [MessageInline]

# 필요 시 MessageAdmin 주석 처리 또는 제거 가능
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ['chatroom', 'sender', 'input_msg', 'created_at']
#     search_fields = ['sender__email', 'input_msg']
#     list_filter = ['chatroom', 'created_at']
