# interest/urls.py
from django.urls import path
from .views import GPTKeywordExtractionView
from .views import GPTKeywordSaveView
from .views import UserKeywordListView

urlpatterns = [
    path("extract-keywords/", GPTKeywordExtractionView.as_view()),
]

urlpatterns += [
    path("save-keywords/", GPTKeywordSaveView.as_view()),
    path("my-keywords/", UserKeywordListView.as_view()),
]