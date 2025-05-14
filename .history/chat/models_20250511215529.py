from django.db import models

class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        'users.CustomUser',  # ✅ 문자열로 지정! settings.AUTH_USER_MODEL 값과 같아야 함
        on_delete=models.CASCADE
    )
    input_msg = models.TextField()
    filtered_msg = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email}: {self.input_msg[:30]}"
