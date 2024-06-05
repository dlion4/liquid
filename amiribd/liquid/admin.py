from django.contrib import admin

# Register your models


from .models import CompanyTermsAndPolicy


@admin.register(CompanyTermsAndPolicy)
class CompanyTermsAndPolicyAdmin(admin.ModelAdmin):
    list_display = [
        'file',
        'created_at',
        'updated_at',
    ]