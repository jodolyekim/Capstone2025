from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Profile, Guardian, Photo,
    InterestCategory, Interest, InterestKeywordCategoryMap,
    SuggestedInterest, Match, ChatRoom, Message,
    AutoCloseMessage, BadWordsLog
)

# Profile을 UserAdmin 내부에 inline으로 보여주기
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['email']
    ordering = ['id']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('날짜', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    inlines = (ProfileInline,)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'birth_date', 'gender', 'sexual_orientation','communication_styles',
        'latitude', 'longitude','match_distance_km'
    )
    search_fields = ('user__email', 'name')
    list_filter = ('gender', 'sexual_orientation')

# 기타 모델 등록
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
