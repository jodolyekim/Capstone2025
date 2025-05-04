from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    approval_status = models.CharField(max_length=20, default='pending')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    sexual_orientation = models.CharField(max_length=20)
    communication_styles = models.TextField()
    match_distance_km = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class Guardian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=False)
    family_certificate_url = models.TextField()
    disability_certificate_url = models.TextField()

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_url = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InterestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    source = models.CharField(max_length=20)

class InterestKeywordCategoryMap(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)

class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    display_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user2')
    status_user1 = models.CharField(max_length=10)
    status_user2 = models.CharField(max_length=10)
    is_matched = models.BooleanField(default=False)
    matched_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=20, default='text')

class AutoCloseMessage(models.Model):
    content = models.TextField()
    is_default = models.BooleanField(default=True)

class BadWordsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    bad_word = models.CharField(max_length=50)
    filtered_at = models.DateTimeField(auto_now_add=True)
