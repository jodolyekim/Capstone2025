from django.urls import path
from . import views

urlpatterns = [
    path('respond/', views.respond_to_match, name='respond_to_match'),
    path('initiate/', views.initiate_match, name='initiate_match'),
    path('candidates/', views.get_candidates, name='get_candidates'),
]
