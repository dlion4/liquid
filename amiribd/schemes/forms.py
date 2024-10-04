from django import forms
from .models import WhatsAppEarningScheme


class WhatsAppEarningSchemeForm(forms.ModelForm):
    class Meta:
        model = WhatsAppEarningScheme
        fields = ["views", "file"]
        widgets = {
            "views": forms.NumberInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-file-input"}),
        }
        labels = {
            "views": "Input the number of views",
            "file": "Upload Screenshot",
        }
        help_texts = {
            "views": "Input the correct value that matches the screenshot number of views count",
            "file": "Submmit screenshot which is not edited, cropped, faked, cut, manipulated, or otherwise your account will be at risk",
        }
