from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 모델 확장
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_profile_set = models.BooleanField(default=False)

    # 이메일을 ID처럼 사용
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # createsuperuser 시 username도 입력해야 함

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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Step 1: 기본 정보
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    sexual_orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES)

    # Step 2: 커뮤니케이션 선호
    communication_styles = models.JSONField(default=list)  # 예: ["TEXT", "VOICE"]

    # Step 3: 위치 정보
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    distance_preference_km = models.IntegerField(default=5)  # 거리 범위 (최대 600km)

    # Step 4: 사진 업로드 (최대 4장)
    photo_urls = models.JSONField(default=list)  # Firebase 업로드 후 URL 저장

    # Step 5: 자기소개 및 관심 키워드
    bio = models.TextField(max_length=300)
    keywords = models.JSONField(default=list)  # GPT로 추출 + 수동입력 포함

    # Step 6: 보호자 정보
    guardian_name = models.CharField(max_length=100)
    guardian_birthdate = models.DateField()
    guardian_phone = models.CharField(max_length=20)
    guardian_relationship = models.CharField(max_length=50)
    guardian_documents = models.JSONField(default=dict)  # ex) {"relation_cert": "url", "disability_cert": "url"}
    guardian_agreement = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)  # 수동 승인 여부

    def __str__(self):
        return f"{self.user.username}'s Profile"
