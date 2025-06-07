from django.apps import AppConfig

class ChatConfig(AppConfig):
    # 기본 자동 필드 타입 설정 (BigAutoField는 ID에 적합)
    default_auto_field = 'django.db.models.BigAutoField'

    # 앱 이름 지정 (chat 앱 디렉토리와 일치)
    name = 'chat'
