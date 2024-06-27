from collections.abc import Mapping
from typing import Any
from django import forms

from amiribd.invest.types import PlanTypeObjects
from amiribd.users.models import Profile
from .models import AccountWithdrawalAction, Pool, Plan, Account, PoolType
from .models import PlanType, AccountType
from amiribd.transactions.models import PaymentMethod
from unfold.widgets import (
    UnfoldAdminEmailInputWidget, 
    UnfoldAdminTextInputWidget, 
    UnfoldAdminDecimalFieldWidget,
    UnfoldAdminSelectWidget,
    UnfoldBooleanSwitchWidget,
    UnfoldRelatedFieldWidgetWrapper,
    UnfoldForeignKeyRawIdWidget,
    UnfoldAdminSplitDateTimeVerticalWidget,
    UnfoldAdminBigIntegerFieldWidget,
    UnfoldAdminFileFieldWidget,
    UnfoldAdminTextareaWidget
)
from amiribd.transactions.models import Transaction
from unfold.contrib.forms.widgets import WysiwygWidget

class PoolRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "pool-type-id",
                "name": "pool-type",
            }
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
                id__in=user_selected_pool_type
            )


class AccountRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "account-type-id",
                "name": "account-type",
            }
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
                id__in=user_selected_account_type
            )


class PlanRegistrationForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset=PlanType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control select",
                "id": "plan-type-id",
                "name": "plan-type",
            }
        ),
        label="Plan Selction",
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
                    account__pool__profile=self.request.user.profile_user
                )
                .all()
                .values_list("type_id", flat=True)
            )

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_plan_type
            )


class PaymentOptionForm(forms.Form):
    # channel = forms.ModelChoiceField(
    #     queryset=PaymentMethod.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}),
    # )
    pass


class AccountEventWithdrawalForm(forms.ModelForm):
    withdrawal_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "id": "edit-event-start-date",
                "class": "form-control date-picker form-control-lg",
                "data-date-format": "yyyy-mm-dd",
            }
        )
    )
    withdrawal_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "text",
                "id": "edit-event-start-time",
                "data-time-format": "HH:mm:ss",
                "class": "form-control time-picker form-control-lg",
            }
        )
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
            }
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
                }
            ),
            "payment_phone_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Phone Number",
                }
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
            }
        ),
    )


class AddPlanForm(forms.ModelForm):
    price = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "form-control form-control-lg",
            }
        )
    )

    type = forms.ModelChoiceField(
        queryset=PlanType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg",
                "id": "plan-type-choice",
                "name": "plan-type",
                "required": "",
            }
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
        super(AddPlanForm, self).__init__(*args, **kwargs)
        # Now you can use self.request to access request object properties like user
        if (
            self.request
            and self.request.user.is_authenticated
            and self.request.user.profile_user
            and hasattr(self.request.user, 'profile_user')
        ):
            profile_user = self.request.user.profile_user
            user_selected_type_ids = profile_user.plans.values_list("type_id", flat=True)
            # user_selected_type_id = (
            #     Plan.objects.filter(
            #         account__pool__profile=self.request.user.profile_user,
                    
            #     )
            #     .all()
            #     .values_list("type_id", flat=True)
            # )

            self.fields["type"].queryset = self.fields["type"].queryset.exclude(
                id__in=user_selected_type_ids
            )


from .models import PlanStatus


class AdminAddPlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = "__all__"

        widgets = {
            "account":UnfoldAdminSelectWidget(choices=Account.objects.all()),
            "type":UnfoldAdminSelectWidget(choices=PlanType.objects.all()),
            "min_amount":UnfoldAdminDecimalFieldWidget(),
            "max_amount":UnfoldAdminDecimalFieldWidget(),
            "fee":UnfoldAdminDecimalFieldWidget(),
            "status":UnfoldAdminSelectWidget(choices=PlanStatus.choices),
            "payment_method":UnfoldAdminTextInputWidget(),
            "sku":UnfoldAdminTextInputWidget(),
            "is_paid":UnfoldBooleanSwitchWidget(),
            "mpesa_transaction_code":UnfoldAdminTextInputWidget(),
            "payment_phone_number":UnfoldAdminTextInputWidget(),
        }

class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        widgets = {
            "pool": UnfoldAdminSelectWidget(choices=Pool.objects.all()),
            "type": UnfoldAdminSelectWidget(choices=AccountType.objects.all()),
            "created_at": UnfoldAdminSplitDateTimeVerticalWidget(),
            "updated_at": UnfoldAdminSplitDateTimeVerticalWidget(),
            "balance": UnfoldAdminDecimalFieldWidget(),
            "account_ssid": UnfoldAdminTextInputWidget(),
        }

class AdminAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = "__all__"
        widgets = {
            "type":UnfoldAdminSelectWidget(choices=(("Basic", "Basic"), ("Standard", "Standard"))),
            "price":UnfoldAdminDecimalFieldWidget(),
        }


class AdminPoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = "__all__"
        widgets = {
            "profile":UnfoldAdminSelectWidget(choices=Profile.objects.all()),
            "type": UnfoldAdminSelectWidget(choices=PoolType.objects.all()),
            "created_at": UnfoldAdminSplitDateTimeVerticalWidget(),
            "updated_at": UnfoldAdminSplitDateTimeVerticalWidget(),
        }


class AdminTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        widgets = {
            "profile":UnfoldAdminSelectWidget(choices=Profile.objects.all()),
            "account":UnfoldAdminSelectWidget(choices=Account.objects.all()),
            "type": UnfoldAdminTextInputWidget(),
            "created_at": UnfoldAdminSplitDateTimeVerticalWidget(),
            "updated_at": UnfoldAdminSplitDateTimeVerticalWidget(),
            "amount": UnfoldAdminDecimalFieldWidget(),
            "discount": UnfoldAdminDecimalFieldWidget(),
            "paid": UnfoldAdminDecimalFieldWidget(),
            "verified":UnfoldBooleanSwitchWidget(),
            "is_payment_success":UnfoldBooleanSwitchWidget(),
            "receipt_number":UnfoldAdminTextInputWidget(),
            "source":UnfoldAdminTextInputWidget(),
            "payment_phone":UnfoldAdminTextInputWidget(),
            "mpesa_transaction_code":UnfoldAdminTextInputWidget(),
            "payment_phone_number":UnfoldAdminTextInputWidget(),
            "currency":UnfoldAdminTextInputWidget(),
            "country":UnfoldAdminTextInputWidget(),
        }





class AdminPlanTypeForm(forms.ModelForm):
    class Meta:
        model = PlanType
        fields = "__all__"
        widgets = {
            "type":UnfoldAdminSelectWidget(choices=PlanTypeObjects.choices),
            "price":UnfoldAdminDecimalFieldWidget(),
            "percentage_return":UnfoldAdminBigIntegerFieldWidget(),
            "icon":UnfoldAdminTextInputWidget(),
            "svg":UnfoldAdminFileFieldWidget(),
            "interval":UnfoldAdminTextInputWidget(),
            "description":WysiwygWidget()
        }


