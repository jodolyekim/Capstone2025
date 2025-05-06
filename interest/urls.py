# interest/urls.py
from django.urls import path
from .views import GPTKeywordExtractionView
from .views import GPTKeywordSaveView

urlpatterns = [
    path("extract-keywords/", GPTKeywordExtractionView.as_view()),
]

urlpatterns += [
    path("save-keywords/", GPTKeywordSaveView.as_view()),
]