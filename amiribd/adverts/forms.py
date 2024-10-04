from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget

from .models import AdCategory
from .models import Advert


class AdCategoryForm(forms.ModelForm):
    class Meta:
        model = AdCategory
        fields = ["title"]
        widgets = {
            "title": UnfoldAdminTextInputWidget(),
        }

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            "category",
            "title",
            "description",
            "design",
            "website_url",
            "is_approved",
            "is_active",
        ]

