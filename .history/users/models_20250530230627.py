from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# 사용자 정의 매니저: 이메일을 USERNAME_FIELD로 사용하는 CustomUser를 생성
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


# 커스텀 유저 모델: username 필드 제거, 이메일 로그인 사용
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


# 관심사 모델
class Interest(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


# 프로필 모델: 사용자 추가 정보를 관리
class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )

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

    preferred_gender = models.CharField(
        max_length=10,
        choices=[('male', '남성'), ('female', '여성'), ('other', '기타')],
        null=True,
        blank=True
    )
    preferred_orientation = models.CharField(
        max_length=20,
        choices=[
            ('heterosexual', '이성애자'),
            ('homosexual', '동성애자'),
            ('bisexual', '양성애자')
        ],
        null=True,
        blank=True
    )

    # 추가: 관심사와 M2M 연결
    interests = models.ManyToManyField(Interest, blank=True, related_name='profiles')

    def __str__(self):
        return f"{self.user.email}의 프로필"

    def is_complete(self):
        return bool(
            self._name and self._birthYMD and self._gender and self._sex_orientation
        )


# 보호자 모델: 여러 보호자 정보 저장 가능
class Guardian(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='guardians'
    )
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)
    family_certificate_url = models.URLField(blank=True, null=True)
    disability_certificate_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}의 보호자: {self.name}"
