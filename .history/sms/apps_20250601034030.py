from django.apps import AppConfig

class SmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms'  # ← 실제 앱 폴더 이름
