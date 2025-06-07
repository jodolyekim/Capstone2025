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

class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='chatroom')
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')

class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)

class BadWordsLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badwords_logs')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='badwords')
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
