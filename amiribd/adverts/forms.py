from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldBooleanSwitchWidget, UnfoldAdminFileFieldWidget, UnfoldAdminSelectWidget
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import AdCategory, Advert
from django import forms

class AdCategoryForm(forms.ModelForm):
    class Meta:
        model = AdCategory
        fields = ['title']
        widgets = {
            'title': UnfoldAdminTextInputWidget(),	
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

        # widgets = {
        #     'category':UnfoldAdminSelectWidget(choices=AdCategory.objects.all()),
        #     'title': UnfoldAdminTextInputWidget(),	
        #     'website_url': UnfoldAdminTextInputWidget(),	
        #     "description": WysiwygWidget(),
        #     "is_approved":UnfoldBooleanSwitchWidget(),
        #     "is_active":UnfoldBooleanSwitchWidget(),
        #     "design":UnfoldAdminFileFieldWidget(),
        # }
    
