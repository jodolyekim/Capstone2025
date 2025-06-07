from django.contrib import admin
from .models import ChatRoom, Message

# ✅ 메시지를 채팅방 상세 화면에서 인라인으로 표시
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0  # 기본 표시 행 수 없음
    readonly_fields = ('sender', 'input_msg', 'msg_type', 'created_at')  # 읽기 전용 필드
    can_delete = False  # 인라인에서 삭제 비활성화

# ✅ ChatRoom 관리자 설정
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'created_at']
    search_fields = ['chatroom']
    list_filter = ['created_at']
    inlines = [MessageInline]

# ✅ Message 개별 관리 화면: 필터링 관련 정보 표시
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chatroom',
        'sender',
        'msg_type',
        'input_msg',
        'format_filtered',     # 형식 필터 여부
        'gpt_filtered',        # GPT 필터 여부
        'reason',              # 차단 사유
        'created_at',
    ]
    search_fields = ['sender__email', 'input_msg']
    list_filter = [
        'chatroom',
        'msg_type',
        'format_filtered',
        'gpt_filtered',
        'reason',
        'created_at',
    ]
    readonly_fields = ['created_at']  # 안전하게 보기 전용으로 설정
