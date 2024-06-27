from django import forms
from unfold.widgets import UnfoldAdminDecimalFieldWidget, UnfoldAdminTextInputWidget, UnfoldAdminIntegerFieldWidget
from .models import KenyaConversion, Country


class KenyaConversionForm(forms.ModelForm):
    class Meta:
        model = KenyaConversion
        fields = ['currency']
        widgets = {
            'currency':UnfoldAdminTextInputWidget(attrs={"placeholder":"KES"})
        }

class CountryInlineForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
        "country",
        "currency_code",
        "currency_name",
        "amount"
        ]

        widgets = {
            "country": UnfoldAdminTextInputWidget(),
            "currency_code": UnfoldAdminTextInputWidget(),
            "currency_name": UnfoldAdminTextInputWidget(),
            "amount":UnfoldAdminDecimalFieldWidget(attrs={"placeholder":"In relation to 1 KShs" }),
            "conversion_rate": UnfoldAdminDecimalFieldWidget()
        }