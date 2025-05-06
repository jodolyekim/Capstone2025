from django.contrib import admin
from .models import Interest, InterestCategory, InterestKeywordCategoryMap

admin.site.register(Interest)
admin.site.register(InterestCategory)
admin.site.register(InterestKeywordCategoryMap)
