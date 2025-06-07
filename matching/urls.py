from django.urls import path
from .views import (
    respond_to_match,
    initiate_match,
    get_candidates,
)

urlpatterns = [
    path('respond/', respond_to_match, name='respond_to_match'),
    path('initiate/', initiate_match, name='initiate_match'),
    path('candidates/', get_candidates, name='get_candidates'),
]
