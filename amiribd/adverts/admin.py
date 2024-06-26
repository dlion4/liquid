from django.contrib import admin

# Register your models here.
from .models import AdCategory, Advert

@admin.register(AdCategory)
class AdCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "title",
        'is_approved',
        'is_active',
        "description",
        "created_at",
        "updated_at",
        "design",
        "website_url",
    ]
    search_fields = [
        'title',
        'category',
    ]
    list_filters = [
        'is_approved',
        'is_active',
    ]
    actions = (
        "__approve_advert",
        "__disapprove_advert"
    )

    @admin.action(description="Approve")
    def __approve_advert(self, request, queryset):
        queryset.update(is_approved=True)

    
    @admin.action(description="Disaprove")
    def __disapprove_advert(self, request, queryset):
        queryset.update(is_approved=False)

    