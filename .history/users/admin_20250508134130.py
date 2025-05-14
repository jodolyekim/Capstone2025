from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Profile, Guardian, Photo,
    InterestCategory, Interest, InterestKeywordCategoryMap,
    SuggestedInterest, Match, ChatRoom, Message,
    AutoCloseMessage, BadWordsLog
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'username', 'is_active', 'is_staff']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['email', 'username']
    ordering = ['id']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'sexual_orientation', 'latitude', 'longitude', 'distance_preference_km', 'is_verified')
    search_fields = ('user__email',)
    list_filter = ('gender', 'sexual_orientation', 'is_verified')

admin.site.register(Guardian)
admin.site.register(Photo)
admin.site.register(InterestCategory)
admin.site.register(Interest)
admin.site.register(InterestKeywordCategoryMap)
admin.site.register(SuggestedInterest)
admin.site.register(Match)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(AutoCloseMessage)
admin.site.register(BadWordsLog)
