from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# 사용자 정의 매니저: 이메일 기반 사용자 생성 로직 정의
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

# 커스텀 유저 모델 (기본 username 제거, 이메일 기반 로그인)
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_profile_set = models.BooleanField(default=False)  # 프로필 설정 여부 저장
    created_at = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

# 사용자 프로필 모델 (추가 정보 포함)
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    # 기본 정보
    _name = models.CharField(max_length=50, blank=True, null=True)
    _birthYMD = models.DateField(blank=True, null=True)
    _gender = models.CharField(max_length=10, blank=True, null=True)
    _sex_orientation = models.CharField(max_length=20, blank=True, null=True)

    # 선호 커뮤니케이션 방식 (리스트 형태)
    _communication_way = models.JSONField(default=list, blank=True)

    # 위치 정보 및 매칭 거리
    _current_location_lat = models.FloatField(null=True, blank=True)
    _current_location_lon = models.FloatField(null=True, blank=True)
    _match_distance = models.IntegerField(default=5, null=True, blank=True)

    # 보호자 정보
    _protector_info_name = models.CharField(max_length=100, default='홍길동')
    _protector_info_birth_date = models.DateField(null=True, blank=True)
    _protector_info_phone = models.CharField(max_length=20, default='010-0000-0000')
    _protector_info_relationship = models.CharField(max_length=50, default='보호자')

    # ✅ 회원가입 승인 여부
    is_approved = models.BooleanField(default=False)  # 관리자 승인 후 True
    is_rejected = models.BooleanField(default=False)  # 관리자 반려 시 True

    def __str__(self):
        return f"{self.user.email}의 프로필"

    def is_complete(self):
        """ 프로필이 완전히 작성되었는지 여부 반환 """
        return bool(self._name and self._birthYMD and self._gender and self._sex_orientation)

# 보호자 모델 (사용자와 다대일 관계)
class Guardian(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guardians')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)

    # ✅ 이 두 줄 수정
    family_certificate_url = models.URLField(blank=True, null=True)
    disability_certificate_url = models.URLField(blank=True, null=True)


# 사용자 업로드 사진
class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

# 관심사 카테고리 (음악, 게임 등)
class InterestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 사용자 관심 키워드 (자유 입력 또는 GPT 추천 기반)
class Interest(models.Model):
    user = models.ForeignKey(CustomUser, related_name='interests', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)  # ✅ 추가
    source = models.CharField(max_length=10, choices=[('gpt', 'GPT'), ('manual', 'Manual')])


# 키워드와 카테고리 매핑
class InterestKeywordCategoryMap(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='interest_mappings')

# GPT 기반 추천 키워드
class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='suggested_interests')
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

# 매칭 정보 (user1, user2는 CustomUser)
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
    matched_keywords = models.JSONField()  # 예: ["독서", "산책"]
    is_matched = models.BooleanField(default=False)
    matched_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

# 매칭 후 생성되는 채팅방
'''
class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='chatroom')
    participants = models.ManyToManyField('CustomUser', related_name='chatrooms')  # ✅ 이 줄 추가
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

# 채팅 메시지
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')  # 'text', 'image' 등
'''
# 시스템 자동 종료 메시지
class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)

# 욕설 필터 로그 (어떤 유저가 어떤 욕을 언제 썼는지 저장)
class BadWordsLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badwords_logs')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='badwords')
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
