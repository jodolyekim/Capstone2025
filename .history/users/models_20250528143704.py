from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# 사용자 정의 매니저
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

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_profile_set = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    _name = models.CharField(max_length=50, blank=True, null=True)
    _birthYMD = models.DateField(blank=True, null=True)
    _gender = models.CharField(max_length=10, blank=True, null=True)
    _sex_orientation = models.CharField(max_length=20, blank=True, null=True)
    _communication_way = models.JSONField(default=list, blank=True)
    _current_location_lat = models.FloatField(null=True, blank=True)
    _current_location_lon = models.FloatField(null=True, blank=True)
    _match_distance = models.IntegerField(default=5, null=True, blank=True)
    _protector_info_name = models.CharField(max_length=100, default='홍길동')
    _protector_info_birth_date = models.DateField(null=True, blank=True)
    _protector_info_phone = models.CharField(max_length=20, default='010-0000-0000')
    _protector_info_relationship = models.CharField(max_length=50, default='보호자')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}의 프로필"

    def is_complete(self):
        return bool(self._name and self._birthYMD and self._gender and self._sex_orientation)

class Guardian(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guardians')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)
    family_certificate_url = models.URLField(blank=True, null=True)
    disability_certificate_url = models.URLField(blank=True, null=True)

class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InterestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Interest(models.Model):
    user = models.ForeignKey(CustomUser, related_name='interests', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=10, choices=[('gpt', 'GPT'), ('manual', 'Manual')])

class InterestKeywordCategoryMap(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='interest_mappings')

class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='suggested_interests')
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

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

class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)

class BadWordsLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badwords_logs')
    message = models.ForeignKey(
        "chat.Message",  # ✅ 순환 참조 방지를 위한 문자열 참조
        on_delete=models.CASCADE,
        related_name='badwords'
    )
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
