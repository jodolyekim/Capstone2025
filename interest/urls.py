# interest/urls.py
from django.urls import path
from .views import GPTKeywordExtractionView

urlpatterns = [
    path("extract-keywords/", GPTKeywordExtractionView.as_view()),
]

