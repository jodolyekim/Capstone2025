from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InterestCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Interest Categories"

    def __str__(self):
        return self.name


class Interest(models.Model):
    keyword = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interest_interests')
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'keyword')
        verbose_name_plural = "Interests"

    def __str__(self):
        return f"{self.user.email} - {self.keyword}"


class InterestKeywordCategoryMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'interest', 'category')
        verbose_name_plural = "Interest-Category Mappings"

    def __str__(self):
        return f"{self.user.email} - {self.interest.keyword} → {self.category.name}"

class SuggestedInterest(models.Model):
    keyword = models.CharField(max_length=100)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Suggested Interests"
        unique_together = ('keyword', 'category')

    def __str__(self):
        return f"{self.keyword} ({self.category.name})"
