from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Guardian

# Profile 모델을 CustomUser 관리자 페이지에서 inline으로 표시
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ('_name', '_birthYMD', '_gender', '_sex_orientation')

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
        'user', '_name', '_birthYMD', '_gender', '_sex_orientation',
        'pretty_communication_way',
        '_current_location_lat', '_current_location_lon', '_match_distance',
        'is_approved', 'is_rejected'   # ✅ is_approved → is_verified, 거절이면 is_rejected
    )
    search_fields = ('user__email', '_name')
    list_filter = ('_gender', '_sex_orientation', 'is_approved', 'is_rejected')  # ✅ 동일하게
    list_editable = ('is_approved', 'is_rejected')  # ✅ 승인/거절 직접 수정

    def pretty_communication_way(self, obj):
        """JSON 형태의 소통 스타일을 보기 좋게 표시"""
        if not obj._communication_way:
            return "-"
        return ", ".join(obj._communication_way)
    pretty_communication_way.short_description = "소통 스타일"

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('display_user_guardian', 'phone', 'relation', 'is_visible')
    search_fields = ('user__email', 'name')
    list_filter = ('is_visible',)
    list_editable = ('is_visible',)

    def display_user_guardian(self, obj):
        """회원 이메일 - 보호자 이름 같이 표시"""
        return f"{obj.user.email} - {obj.name}"
    display_user_guardian.short_description = "회원 이메일 - 보호자 이름"
