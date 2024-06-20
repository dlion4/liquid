from django.contrib import admin
from .models import KenyaConversion, Country
# Register your models here.

class CountryInline(admin.StackedInline):
    model = Country
    extra = 0



@admin.register(KenyaConversion)
class KenyaConversionAdmin(admin.ModelAdmin):
    inlines = [CountryInline]
