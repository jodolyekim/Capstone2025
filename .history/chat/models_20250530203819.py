from django.db import models
from django.contrib.auth import get_user_model
from chat.models import ChatRoom  # ✅ ChatRoom을 chat 앱에서 import

User = get_user_model()


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
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
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.sender.email} ({self.msg_type}): {self.input_msg[:30]}"


class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[신고] {self.reporter.email} → 메시지 ID {self.message.id}"


class AutoCloseMessage(models.Model):
    content = models.TextField("자동 종료 안내 메시지")
    is_default = models.BooleanField("기본 메시지 여부", default=False)

    def __str__(self):
        return self.content[:30]


class BadWordsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bad_word = models.CharField(max_length=100)
    filtered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.bad_word}"
