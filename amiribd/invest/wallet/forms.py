from django import forms

from amiribd.invest.models import Account


class TransferMoneyForm(forms.Form):
    destination_account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        empty_label="Destination Account",
        widget=forms.Select(attrs={"class": "form-control form-control-lg"}),
    )
    amount_to_transfer = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Amount to transfer",
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields["destination_account"].queryset = Account.objects.exclude(
                pool__profile=self.request.user.profile_user,
            )
