# matching/urls.py

from django.urls import path
from matching.views import MatchingCandidatesAPIView

urlpatterns = [
    path('candidates/', MatchingCandidatesAPIView.as_view(), name='match-candidates'),
]
