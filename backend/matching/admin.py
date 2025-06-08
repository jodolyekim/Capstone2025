from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user1_email',
        'user2_email',
        'status_user1',
        'status_user2',
        'is_matched',
        'matched_at',
        'matched_keywords_display',
    )
    list_filter = ('is_matched', 'status_user1', 'status_user2')
    search_fields = ('user1__email', 'user2__email')
    ordering = ('-matched_at',)

    def user1_email(self, obj):
        return obj.user1.email
    user1_email.short_description = 'User1 Email'

    def user2_email(self, obj):
        return obj.user2.email
    user2_email.short_description = 'User2 Email'

    def matched_keywords_display(self, obj):
        return ", ".join(obj.matched_keywords or [])
    matched_keywords_display.short_description = '공통 키워드'
