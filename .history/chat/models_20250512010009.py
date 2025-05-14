from django.db import models

class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        'users.CustomUser',  # ✅ 사용자 모델 연결
        on_delete=models.CASCADE
    )
    input_msg = models.TextField()
    filtered_msg = models.TextField(blank=True, null=True)
    msg_type = models.CharField(  # ✅ 새 필드: 텍스트 / 이미지 구분
        max_length=10,
        choices=[('text', 'Text'), ('image', 'Image')],
        default='text'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} ({self.msg_type}): {self.input_msg[:30]}"
