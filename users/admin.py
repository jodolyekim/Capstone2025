from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Profile, Guardian, Photo,
    InterestCategory, Interest, InterestKeywordCategoryMap,
    SuggestedInterest, Match, ChatRoom, Message,
    AutoCloseMessage, BadWordsLog
)

# Profile 모델을 CustomUser 관리자 페이지에서 inline으로 보여주기 위한 설정
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# CustomUser 모델을 Django 관리자에 등록
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']  # 목록에서 보여줄 필드
    list_filter = ['is_staff', 'is_superuser']  # 필터 항목
    search_fields = ['email']  # 검색 가능 필드
    ordering = ['id']  # 기본 정렬 순서

    # 사용자 정보 수정 시 보여지는 필드셋 구성
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
        ('날짜', {'fields': ('last_login', 'date_joined')}), 
    )

    # 사용자 추가 시 보여지는 필드셋 구성
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # 사용자 정보 수정 페이지에 ProfileInline 포함
    inlines = (ProfileInline,)

    # 사용자 추가 시 inline 미표시 방지
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Profile 모델을 별도로 관리자로 등록
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', '_name', '_birthYMD', '_gender', '_sex_orientation',
        'pretty_communication_way',
        '_current_location_lat', '_current_location_lon', '_match_distance'
    )
    search_fields = ('user__email', '_name')  # 이메일과 이름으로 검색
    list_filter = ('_gender', '_sex_orientation')  # 필터 항목

    # _communication_way를 보기 쉽게 변환
    def pretty_communication_way(self, obj):
        if not obj._communication_way:
            return "-"
        return ", ".join(obj._communication_way)
    pretty_communication_way.short_description = "소통 스타일"

# 그 외 기타 모델들을 관리자에 등록
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
