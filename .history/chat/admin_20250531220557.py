from django.contrib import admin
from .models import ChatRoom, Message, Report, ChatReport
from matching.models import Match

# ✅ 메시지를 채팅방 상세 화면에서 인라인으로 표시
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = (
        'sender', 'input_msg', 'msg_type', 'created_at',
        'format_filtered', 'gpt_filtered', 'reason'
    )
    can_delete = False
    show_change_link = True


# ✅ ChatRoom 관리자 설정
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['chatroom', 'match_link', 'created_at', 'participant_emails']
    search_fields = ['chatroom']
    list_filter = ['created_at']
    inlines = [MessageInline]

    def match_link(self, obj):
        if obj.match:
            return f"Match ID {obj.match.id} ({obj.match.user1.email} ↔ {obj.match.user2.email})"
        return "연결 안됨"
    match_link.short_description = "연결된 매칭"

    def participant_emails(self, obj):
        return ", ".join([u.email for u in obj.participants.all()])
    participant_emails.short_description = "참여 유저 이메일"


# ✅ Message 개별 관리 화면: 필터링 관련 정보 표시
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chatroom', 'sender', 'msg_type', 'input_msg',
        'format_filtered', 'gpt_filtered', 'reason', 'created_at',
    ]
    search_fields = ['sender__email', 'input_msg']
    list_filter = ['msg_type', 'format_filtered', 'gpt_filtered', 'reason', 'created_at']
    readonly_fields = ['chatroom', 'sender', 'created_at']


# ✅ Report (메시지 단위 신고)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'message', 'reason', 'reported_at']
    search_fields = ['reporter__email', 'reason']
    readonly_fields = ['reported_at']
    list_filter = ['reported_at']


# ✅ ChatReport (채팅방 단위 신고)
@admin.register(ChatReport)
class ChatReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'reported', 'reason', 'timestamp', 'is_resolved']
    list_filter = ['reason', 'is_resolved']
    search_fields = ['reporter__email', 'reported__email', 'custom_reason']
    readonly_fields = [
        'reporter', 'reported', 'chat_room', 'reason',
        'custom_reason', 'message_snapshot', 'timestamp'
    ]

    actions = ['mark_as_resolved', 'ban_reported_users']

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f"{updated}건의 신고를 해결 처리했습니다.")

    def ban_reported_users(self, request, queryset):
        for report in queryset:
            user = report.reported
            user.is_active = False
            user.save()
        self.message_user(request, f"{queryset.count()}명의 사용자가 정지되었습니다.")

    mark_as_resolved.short_description = "✅ 선택된 신고를 '해결됨'으로 표시"
    ban_reported_users.short_description = "🚫 선택된 신고 대상 사용자 계정 정지"
