from django.contrib import admin
from .models import Guardian, GuardianAlertLog

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone']
    search_fields = ['user__email', 'name', 'phone']

@admin.register(GuardianAlertLog)
class GuardianAlertLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'guardian', 'event_type', 'phone', 'sent_at']
    list_filter = ['event_type', 'sent_at']
    search_fields = ['user__email', 'guardian__name', 'guardian__phone']
