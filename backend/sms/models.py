from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser, Guardian
from chat.models import Message

class GuardianAlertLog(models.Model):
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='alert_logs')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='alert_logs')  # 보호 대상자
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='alert_logs')
    event_type = models.CharField(max_length=20)  # '사진 전송' 또는 '사진 수신'
    phone = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} → {self.guardian.phone} ({self.event_type})"
