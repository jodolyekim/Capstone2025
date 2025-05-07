from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# 사용자 매니저
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# 사용자 모델
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_profile_set = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# 프로필 모델
class Profile(models.Model):
    GENDER_CHOICES = [('M', '남성'), ('F', '여성'), ('O', '기타')]
    ORIENTATION_CHOICES = [('HETERO', '이성애'), ('HOMO', '동성애'), ('BI', '양성애'), ('OTHER', '기타')]
    COMMUNICATION_CHOICES = [('TEXT', '글로 대화하기'), ('SLOW_SPEECH', '천천히 말해주기'), ('VOICE', '음성 대화')]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
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
        return f"{self.user.email}'s Profile"


# 보호자
class Guardian(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guardians')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)
    family_certificate_url = models.URLField()
    disability_certificate_url = models.URLField()


# 사용자 사진
class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


# 관심사 카테고리
class InterestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# 관심 키워드
class Interest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interests')
    keyword = models.CharField(max_length=100)
    source = models.CharField(max_length=20)


# 키워드와 카테고리 매핑
class InterestKeywordCategoryMap(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='interest_mappings')


# GPT 제안 키워드
class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='suggested_interests')
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)


# 매칭
class Match(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='matches_as_user2')
    status_user1 = models.CharField(max_length=10)
    status_user2 = models.CharField(max_length=10)
    is_matched = models.BooleanField(default=False)
    matched_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)


# 채팅방
class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='chatroom')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)


# 메시지
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')


# 자동 종료 메시지
class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)


# 욕설 필터 로그
class BadWordsLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badwords_logs')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='badwords')
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
