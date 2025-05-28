from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InterestCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Interest(models.Model):
    keyword = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')  # related_name 추가
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'keyword')  # 유저마다 중복 금지

    def __str__(self):
        return f"{self.user.email} - {self.keyword}"


class InterestKeywordCategoryMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자별 연결
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.interest.keyword} → {self.category.name}"
