from django.db import models
from django.contrib.auth import get_user_model

class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')  # ✅ 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE
    )
    input_msg = models.TextField()
    filtered_msg = models.TextField(blank=True, null=True)
    msg_type = models.CharField(
        max_length=10,
        choices=[('text', 'Text'), ('image', 'Image')],
        default='text'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ [추가] 필터링 관련 메타데이터
    format_filtered = models.BooleanField(default=False)  # 형식 필터 감지 여부
    gpt_filtered = models.BooleanField(default=False)     # GPT에서 최종 차단 여부
    reason = models.CharField(max_length=255, blank=True) # 차단 사유 (예: '욕설', '주소')

    def __str__(self):
        return f"{self.sender.email} ({self.msg_type}): {self.input_msg[:30]}"
