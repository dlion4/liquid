from django import forms

from amiribd.transactions.models import PaymentMethod
from amiribd.transactions.models import Transaction

from .models import Account
from .models import AccountType
from .models import AccountWithdrawalAction
from .models import InvestMentSaving
from .models import Plan
from .models import PlanType
from .models import Pool
from .models import PoolType


class PoolRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "pool-type-id",
                "name": "pool-type",
            },
        ),
        queryset=PoolType.objects.all(),
        required=True,
        label="Pool Type",
        help_text="Select the type of pool you would like to create.",
    )

    class Meta:
        model = Pool
        fields = ["type"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.request:
            user_selected_pool_type = (
                Pool.objects.filter(profile=self.request.user.profile_user)
                .all()
                .values_list("type_id", flat=True)
            )

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_pool_type,
            )


class AccountRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "account-type-id",
                "name": "account-type",
            },
        ),
        label="Account Selection",
        help_text="Select an account type for your plan",
    )

    class Meta:
        model = Account
        fields = [
            "type",
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.request:
            user_selected_account_type = (
                Account.objects.filter(pool__profile=self.request.user.profile_user)
                .all()
                .values_list("type_id", flat=True)
            )

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_account_type,
            )


class PlanRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=PlanType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "plan-type-id",
                "name": "plan-type",
            },
        ),
        label="Plan Selection",
        help_text="Select a suitable plan that fits your pocket",
    )

    class Meta:
        model = Plan
        fields = ["type"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

        if self.request:
            user_selected_plan_type = (
                Plan.objects.filter(
                    account__pool__profile=self.request.user.profile_user,
                )
                .all()
                .values_list("type_id", flat=True)
            )

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_plan_type,
            )


class PaymentOptionForm(forms.Form):
    channel = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class AccountEventWithdrawalForm(forms.ModelForm):
    withdrawal_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "id": "edit-event-start-date",
                "class": "form-control date-picker form-control-lg",
                "data-date-format": "yyyy-mm-dd",
            },
        ),
    )
    withdrawal_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "text",
                "id": "edit-event-start-time",
                "data-time-format": "HH:mm:ss",
                "class": "form-control time-picker form-control-lg",
            },
        ),
    )

    channel = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        widget=forms.Select(
            attrs={
                "id": "edit-event-theme",
                "class": "select-calendar-theme form-control select2 form-control-lg",
                "data-search": "on",
                "tabindex": "-1",
                "aria-hidden": "true",
            },
        ),
    )

    class Meta:
        model = AccountWithdrawalAction
        fields = [
            "amount",
            "withdrawal_date",
            "withdrawal_time",
            "channel",
            "payment_phone_number",
        ]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "hx-get": "/htmx/account/available_amount/",
                    "hx-target": "#id_available_amount",
                    "hx-trigger": "keyup changed delay:1s",
                    "type": "number",
                    "class": "form-control form-control-lg",
                    "id": "edit-event-title",
                    "hx-swap": "innerHTML",
                    "hx-swap-oob": "true",
                    "name": "amount",
                    "required": "",
                },
            ),
            "payment_phone_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Phone Number",
                },
            ),
        }


class CancelPlanForm(forms.Form):
    plan = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "id": "plan-type-from-user-input",
                "placeholder": "sample plan",
                "hx-get": "/htmx/account/cancel-plan/",
                "hx-target": "#plan-type-from-db",
                "hx-trigger": "keyup changed delay:1s",
                "hx-swap": "innerHTML",
                "hx-swap-oob": "true",
                "name": "plan",
                "required": "",
            },
        ),
    )


class AddPlanForm(forms.ModelForm):
    price = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "form-control form-control-lg",
            },
        ),
    )

    type = forms.ModelChoiceField(
        queryset=PlanType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg",
                "id": "plan-type-choice",
                "name": "plan-type",
                "required": "",
            },
        ),
        required=True,
        label="Plan Selection",
        help_text="Select a suitable plan that fits your pocket",
        empty_label="No plan available",
    )

    class Meta:
        model = Plan
        fields = [
            "type",
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        # Now you can use self.request to access request object properties like user
        if (
            self.request
            and self.request.user.is_authenticated
            and self.request.user.profile_user
            and hasattr(self.request.user, "profile_user")
        ):
            profile_user = self.request.user.profile_user
            user_selected_type_ids = profile_user.plans.values_list(
                "type_id", flat=True)
            # user_selected_type_id = (  # noqa: ERA001, RUF100
            #     Plan.objects.filter(
            #         account__pool__profile=self.request.user.profile_user,  # noqa: E501, ERA001, RUF100
            #     ) # noqa: ERA001, RUF100
            #     .all()
            #     .values_list("type_id", flat=True)
            # ) # noqa: ERA001, RUF100

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_type_ids,
            )


class AdminAddPlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = "__all__"  # noqa: DJ007


class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"  # noqa: DJ007


class AdminAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = "__all__" # noqa: DJ007


class AdminPoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = "__all__" # noqa: DJ007


class AdminTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__" # noqa: DJ007


class AdminPlanTypeForm(forms.ModelForm):
    class Meta:
        model = PlanType
        fields = "__all__" # noqa: DJ007


class InvestMentSavingForm(forms.ModelForm):
    principal_amount = forms.CharField(widget=forms.HiddenInput())
    duration_of_saving_investment = forms.CharField(widget=forms.HiddenInput())
    interest_amount = forms.CharField(widget=forms.HiddenInput())
    expected_daily_interest_plus_amount = forms.CharField(widget=forms.HiddenInput())
    instruction = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = InvestMentSaving
        fields = [
            "principal_amount",
            "duration_of_saving_investment",
            "interest_amount",
            "expected_daily_interest_plus_amount",
            "instruction",
        ]
