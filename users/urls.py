# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('match/request/', views.create_match_request, name='create_match_request'),
    path('match/respond/<int:match_id>/', views.respond_to_match, name='respond_to_match'),
]
