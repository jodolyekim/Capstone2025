from django.contrib import admin
from .models import GuardianAlertLog

@admin.register(GuardianAlertLog)
class GuardianAlertLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'guardian', 'event_type', 'phone', 'sent_at']
    list_filter = ['event_type', 'sent_at']
    search_fields = ['user__email', 'guardian__name', 'guardian__phone']
