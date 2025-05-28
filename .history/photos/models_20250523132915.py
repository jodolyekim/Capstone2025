from django.db import models

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='images/')  # 로컬에 저장
    uploaded_at = models.DateTimeField(auto_now_add=True)
