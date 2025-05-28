from django.db import models

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='images/')          # 실제 업로드는 Firebase에서 처리
    firebase_url = models.URLField()                        # Firebase에 저장된 이미지 URL
    uploaded_at = models.DateTimeField(auto_now_add=True)