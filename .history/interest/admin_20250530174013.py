from django.contrib import admin
from .models import Interest, InterestCategory, InterestKeywordCategoryMap

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'user', 'source', 'created_at')
    search_fields = ('keyword', 'user__email')
    list_filter = ('source', 'created_at')
    ordering = ('-created_at',)

@admin.register(InterestCategory)
class InterestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(InterestKeywordCategoryMap)
class InterestKeywordCategoryMapAdmin(admin.ModelAdmin):
    list_display = ('user', 'interest', 'category')
    search_fields = ('user__email', 'interest__keyword', 'category__name')
    list_filter = ('category',)
