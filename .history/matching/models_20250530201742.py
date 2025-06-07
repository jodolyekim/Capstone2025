from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기 중'),
        ('accepted', '수락'),
        ('rejected', '거절'),
    ]

    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='matches_as_user2')
    status_user1 = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    status_user2 = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    matched_keywords = models.JSONField()
    is_matched = models.BooleanField(default=False)
    matched_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.email} ↔ {self.user2.email} | 상태: {self.status_user1}/{self.status_user2}"


class ChatRoom(models.Model):
    chatroom = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(CustomUser, related_name='chat_rooms')
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='chatroom', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom: {self.chatroom}"
