from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# 사용자 정의 매니저: 이메일을 USERNAME_FIELD로 사용하는 CustomUser를 생성
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        일반 사용자 생성 메서드
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)  # email 기반 사용자 모델 인스턴스 생성
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        관리자(superuser) 생성 메서드
        """
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
    email = models.EmailField(unique=True)  # 이메일을 고유 식별자로 사용
    is_profile_set = models.BooleanField(default=False)  # 프로필 설정 완료 여부
    created_at = models.DateTimeField(default=timezone.now)  # 가입일시 기록

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 이메일 외 필수 필드 없음

    objects = UserManager()  # 사용자 정의 매니저 등록

    def __str__(self):
        return self.email

# 프로필 모델: 사용자 추가 정보를 관리
class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )  # CustomUser와 일대일 관계

    _name = models.CharField(max_length=50, blank=True, null=True)  # 사용자 이름
    _birthYMD = models.DateField(blank=True, null=True)  # 생년월일 (YYYY-MM-DD)
    _gender = models.CharField(max_length=10, blank=True, null=True)  # 성별
    _sex_orientation = models.CharField(max_length=20, blank=True, null=True)  # 성적 지향

    _communication_way = models.JSONField(default=list, blank=True)  # 선호 대화 방식 (JSON 배열)

    _current_location_lat = models.FloatField(null=True, blank=True)  # 현재 위치 위도
    _current_location_lon = models.FloatField(null=True, blank=True)  # 현재 위치 경도
    _match_distance = models.IntegerField(
        default=5, null=True, blank=True
    )  # 매칭 거리 범위 (km)

    # 보호자 정보 기본값
    _protector_info_name = models.CharField(
        max_length=100, default='홍길동'
    )  # 보호자 이름
    _protector_info_birth_date = models.DateField(null=True, blank=True)  # 보호자 생년월일
    _protector_info_phone = models.CharField(
        max_length=20, default='010-0000-0000'
    )  # 보호자 연락처
    _protector_info_relationship = models.CharField(
        max_length=50, default='보호자'
    )  # 보호자 관계

    is_approved = models.BooleanField(default=False)  # 프로필 검증(승인) 여부
    is_rejected = models.BooleanField(default=False)  # 프로필 거절 여부

    preferred_gender = models.CharField(
        max_length=10,
        choices=[
            ('male', '남성'),
            ('female', '여성'),
            ('other', '기타')
        ],
        null=True,
        blank=True
    )  # 선호하는 성별

    preferred_orientation = models.CharField(
        max_length=20,
        choices=[
            ('heterosexual', '이성애자'),
            ('homosexual', '동성애자'),
            ('bisexual', '양성애자')
        ],
        null=True,
        blank=True
    )  # 선호하는 성적 지향

    def __str__(self):
        return f"{self.user.email}의 프로필"

    def is_complete(self):
        """
        필수 프로필 정보가 모두 채워졌는지 확인
        """
        return bool(
            self._name and self._birthYMD and self._gender and self._sex_orientation
        )

# 보호자 모델: 여러 보호자 정보 저장 가능
class Guardian(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='guardians'
    )  # CustomUser와 다대일 관계
    name = models.CharField(max_length=50)  # 보호자 이름
    phone = models.CharField(max_length=20)  # 보호자 연락처
    relation = models.CharField(max_length=30)  # 보호자와의 관계
    is_visible = models.BooleanField(default=False)  # 보호자 정보 공개 여부
    family_certificate_url = models.URLField(blank=True, null=True)  # 가족관계증명서 URL
    disability_certificate_url = models.URLField(blank=True, null=True)  # 장애인증명서 URL

    def __str__(self):
        return f"{self.user.email}의 보호자: {self.name}"
