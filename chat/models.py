from django.db import models
from users.models import CustomUser, Match  # ✅ 외부 모델 참조

class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='chatroom')
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ChatRoom for Match {self.match.id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')  # 예: 'text', 'image'

    def __str__(self):
        return f"{self.sender.email} at {self.sent_at}"

class BadWordsLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badwords_logs')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='badwords')
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.bad_word}"
