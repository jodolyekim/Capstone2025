# matching/urls.py

from django.urls import path
from .views import MatchingCandidatesAPIView

urlpatterns = [
    path('candidates/', MatchingCandidatesAPIView.as_view(), name='match-candidates'),
    path('chatrooms/', get_chat_rooms, name='chatroom-list'),  # ✅ 추가


]
