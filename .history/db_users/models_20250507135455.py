from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

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

class User(models.Model):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    approval_status = models.CharField(max_length=20, default='pending')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='db_users_profile')
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    sexual_orientation = models.CharField(max_length=20)
    communication_styles = models.TextField()
    match_distance_km = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Guardian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_guardians')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)
    family_certificate_url = models.URLField()
    disability_certificate_url = models.URLField()


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_photos')
    photo_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class InterestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_interests')
    keyword = models.CharField(max_length=100)
    source = models.CharField(max_length=20)


class InterestKeywordCategoryMap(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='db_users_category_mappings')
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='db_users_interest_mappings')


class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='db_users_suggested_interests')
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_matches_as_user2')
    status_user1 = models.CharField(max_length=10)
    status_user2 = models.CharField(max_length=10)
    is_matched = models.BooleanField(default=False)
    matched_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)


class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='db_users_chatroom')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='db_users_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')


class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)


class BadWordsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='db_users_badwords_logs')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='db_users_badwords')
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
