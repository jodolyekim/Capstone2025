from django.contrib import admin
from .models import ChatRoom, Message, BadWordsLog  # ✅ BadWordsLog 추가

# 메시지를 채팅방 상세에서 인라인으로 보여주기
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'message_type', 'sent_at')  # ✅ 필드 이름 통일
    can_delete = False

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'created_at']
    search_fields = ['match__id']
    list_filter = ['created_at']
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'room',
        'sender',
        'message_type',
        'content',
        'sent_at',
    ]
    search_fields = ['sender__email', 'content']
    list_filter = [
        'room',
        'message_type',
        'sent_at'
    ]

@admin.register(BadWordsLog)
class BadWordsLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'bad_word', 'filtered_at']
    search_fields = ['user__email', 'bad_word']
    list_filter = ['filtered_at']
