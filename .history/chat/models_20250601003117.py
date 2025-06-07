from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ ChatRoom 모델
class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    # matching.Match를 문자열로 참조(순환 참조 방지)
    match = models.OneToOneField('matching.Match', on_delete=models.CASCADE, related_name='chatroom', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"


# ✅ Message 모델
class Message(models.Model):
    chatroom = models.ForeignKey("chat.ChatRoom", on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sent_messages')
    input_msg = models.TextField()
    filtered_msg = models.TextField(blank=True, null=True)
    msg_type = models.CharField(
        max_length=10,
        choices=[('text', 'Text'), ('image', 'Image')],
        default='text'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    format_filtered = models.BooleanField(default=False)
    gpt_filtered = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.sender.email} ({self.msg_type}): {self.input_msg[:30]}"


# ✅ 메시지 단위 신고 (기존 구조 유지)
class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[신고] {self.reporter.email} → 메시지 ID {self.message.id}"


# ✅ 자동 종료 메시지
class AutoCloseMessage(models.Model):
    content = models.TextField("자동 종료 안내 메시지")
    is_default = models.BooleanField("기본 메시지 여부", default=False)

    def __str__(self):
        return self.content[:30]


# ✅ 욕설 필터링 로그
class BadWordsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bad_word = models.CharField(max_length=100)
    filtered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.bad_word}"


# ✅ 채팅방 단위 신고 모델 (신규 추가)
class ChatReport(models.Model):
    REPORT_REASON_CHOICES = [
        ('abuse', '욕설/폭언'),
        ('sexual', '성적 발언'),
        ('privacy', '개인정보 요구'),
        ('other', '기타'),
    ]

    reporter = models.ForeignKey(User, related_name='chat_reports_made', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='chat_reports_received', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASON_CHOICES)
    custom_reason = models.TextField(blank=True, null=True)
    message_snapshot = models.TextField()  # 최근 채팅 로그 요약
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reporter.email} → {self.reported.email} ({self.get_reason_display()})"
