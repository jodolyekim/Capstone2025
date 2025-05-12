# UserProfile, Match
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keywords = models.JSONField(default=list)
    
class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    from_user = models.ForeignKey(User, related_name='sent_matches', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_matches', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
# UserProfile에 키워드를 JSON 배열로 저장
# Match 테이블에서 누가 누구에게 요청했는지, 상태가 무엇인지 관리
    