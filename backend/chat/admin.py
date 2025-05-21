from django.contrib import admin
from .models import ChatRoom, Message

# 메시지를 채팅방 상세에서 인라인으로 보여주기
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'input_msg', 'msg_type', 'created_at')
    can_delete = False

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'created_at']
    search_fields = ['chatroom']
    list_filter = ['created_at']
    inlines = [MessageInline]

# ✅ 메시지 개별 조회용 관리자 패널 (필터링 정보 포함)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chatroom',
        'sender',
        'msg_type',
        'input_msg',
        'format_filtered',     # 🔥 형식 필터 여부
        'gpt_filtered',        # 🔥 GPT 필터 여부
        'reason',              # 🔥 차단 사유
        'created_at',
    ]
    search_fields = ['sender__email', 'input_msg']
    list_filter = [
        'chatroom',
        'msg_type',
        'format_filtered',
        'gpt_filtered',
        'reason',
        'created_at'
    ]
