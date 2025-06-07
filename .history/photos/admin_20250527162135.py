from django.contrib import admin
from .models import ProfilePhoto

@admin.register(ProfilePhoto)
class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ['profile', 'uploaded_at', 'thumbnail']

    def thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height:60px;" />'
        return "-"
    thumbnail.allow_tags = True
    thumbnail.short_description = "사진 미리보기"
