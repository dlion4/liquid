from django import forms
from .models import Pool, Plan, Account, PoolType
from .models import PlanType, AccountType
from amiribd.transactions.models import PaymentMethod


class PoolRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                "class": "select2 select2-container select2-container--default select2-container--below select2-container--focus"
            }
        ),
        queryset=PoolType.objects.all(),
        required=True,
        initial=PoolType.objects.first(),
        label="Pool Type",
        help_text="Select the type of pool you would like to create.",
    )

    class Meta:
        model = Pool
        fields = ["type"]


class AccountRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 select2-container select2-container--default select2-container--below select2-container--focus"
            }
        ),
        label="Account Seelction",
        help_text="Select an account type for your plan",
    )

    class Meta:
        model = Account
        fields = [
            "type",
        ]


class PlanRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=PlanType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 select2-container select2-container--default select2-container--below select2-container--focus"
            }
        ),
        label="Plan Seelction",
        help_text="Select a suitable plan that fits your pocket",
    )

    class Meta:
        model = Plan
        fields = ["type"]


class PaymentOptionForm(forms.Form):
    channel = forms.ModelChoiceField(queryset=PaymentMethod.objects.all())