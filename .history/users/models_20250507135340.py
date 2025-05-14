from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 모델 확장
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_profile_set = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# 프로필 모델
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]

    ORIENTATION_CHOICES = [
        ('HETERO', '이성애'),
        ('HOMO', '동성애'),
        ('BI', '양성애'),
        ('OTHER', '기타'),
    ]

    COMMUNICATION_CHOICES = [
        ('TEXT', '글로 대화하기'),
        ('SLOW_SPEECH', '천천히 말해주기'),
        ('VOICE', '음성 대화'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='users_profile')

    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    sexual_orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES)
    communication_styles = models.JSONField(default=list)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    distance_preference_km = models.IntegerField(default=5)
    photo_urls = models.JSONField(default=list)
    bio = models.TextField(max_length=300)
    keywords = models.JSONField(default=list)
    guardian_name = models.CharField(max_length=100)
    guardian_birthdate = models.DateField()
    guardian_phone = models.CharField(max_length=20)
    guardian_relationship = models.CharField(max_length=50)
    guardian_documents = models.JSONField(default=dict)
    guardian_agreement = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
