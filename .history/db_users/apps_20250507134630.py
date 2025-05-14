from django.apps import AppConfig

class DbUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db_users'
    label = 'db_users'  # 🔥 이 줄을 반드시 추가
