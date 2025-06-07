from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'is_matched', 'matched_at')
    list_filter = ('is_matched',)
    search_fields = ('user1__email', 'user2__email')
