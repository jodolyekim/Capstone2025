from django.db import models
from django.contrib.auth import get_user_model  # ✅ 이거 꼭 추가
User = get_user_model()  # ✅ 이거도 꼭 위 import 아래에 선언

class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')  # ✅ 여기 사용됨
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
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
