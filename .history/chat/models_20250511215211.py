from django.db import models
from django.contrib.auth import get_user_model


class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        get_user_model(),  # ✅ 전역 User 제거, 여기에 직접 사용
        on_delete=models.CASCADE
    )
    input_msg = models.TextField()
    filtered_msg = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email}: {self.input_msg[:30]}"
