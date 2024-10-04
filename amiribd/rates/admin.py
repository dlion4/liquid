from django.contrib import admin
from .models import KenyaConversion, Country

# Register your models here.
from .forms import KenyaConversionForm, CountryInlineForm

class CountryInline(admin.StackedInline):
    model = Country
    extra = 0
    form = CountryInlineForm
    



@admin.register(KenyaConversion)
class KenyaConversionAdmin(admin.ModelAdmin):
    inlines = [CountryInline]
    form = KenyaConversionForm
