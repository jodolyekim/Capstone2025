from django.urls import path
from .views import upload_image, send_message  # ✅ 두 함수 등록
from chat import views

urlpatterns = [
    path('upload-image/', upload_image, name='upload_image'),
    path('send-message/', send_message, name='send_message'),
    path('report-message/', views.report_message),
]
