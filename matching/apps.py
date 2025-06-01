from django.apps import AppConfig

# 수정 후 👍
class MatchingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matching'
