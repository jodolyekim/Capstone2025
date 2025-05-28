from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Profile, Guardian, Photo,
    InterestCategory, Interest, InterestKeywordCategoryMap,
    SuggestedInterest, Match, ChatRoom, Message,
    AutoCloseMessage, BadWordsLog
)

# ✅ Profile 모델을 CustomUser 관리자 페이지에서 inline으로 표시
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# ✅ CustomUser 관리자 등록
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

# ✅ Profile 관리자 등록
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', '_name', '_birthYMD', '_gender', '_sex_orientation',
        'pretty_communication_way',
        '_current_location_lat', '_current_location_lon', '_match_distance'
    )
    search_fields = ('user__email', '_name')
    list_filter = ('_gender', '_sex_orientation')

    def pretty_communication_way(self, obj):
        if not obj._communication_way:
            return "-"
        return ", ".join(obj._communication_way)
    pretty_communication_way.short_description = "소통 스타일"

# ✅ Match 관리자 등록
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user1', 'user2',
        'status_user1', 'status_user2',
        'is_matched', 'matched_at', 'requested_at'
    )
    list_filter = ('status_user1', 'status_user2', 'is_matched')
    search_fields = ('user1__email', 'user2__email')
    ordering = ('-requested_at',)

# ✅ ChatRoom 관리자 등록
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'is_active', 'created_at', 'last_message_at')
    search_fields = ('match__user1__email', 'match__user2__email')

# ✅ 기타 모델 일괄 등록
admin.site.register(Guardian)
admin.site.register(Photo)
admin.site.register(InterestCategory)
admin.site.register(Interest)
admin.site.register(InterestKeywordCategoryMap)
admin.site.register(SuggestedInterest)
admin.site.register(Message)
admin.site.register(AutoCloseMessage)
admin.site.register(BadWordsLog)
