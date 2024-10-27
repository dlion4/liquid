from django import forms
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from amiribd.invest.models import Account
from amiribd.users.models import Profile

from .models import AccountDeposit


class AccountDepositModelForm(forms.ModelForm):
    class Meta:
        model = AccountDeposit
        fields = [
            "account",
            "amount",
            "reason",
        ]
        # Define default widgets here
        widgets = {
            "account": forms.Select(attrs={"class": "form-control py-3"}),
            "amount": forms.NumberInput(attrs={
                "class": "form-control py-3", "placeholder": "Enter amount"}),
            "reason": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Reason for deposit"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if isinstance(self.request.user, AnonymousUser):
            profile = None  # Handle case where user is anonymous
        else:
            profile = get_object_or_404(Profile, user=self.request.user)

        if profile.plans.exists():
            self.fields["account"].queryset = Account.objects.filter(
                pool__profile=profile)
            self.fields["account"].initial = Account.objects.filter(
                pool__profile=profile).first()
            self.fields["account"].empty_label = None
        self.fields["account"].widget.attrs.update({"class": "form-control py-3"})

