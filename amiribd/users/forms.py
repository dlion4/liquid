from django import forms
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from unfold.widgets import UnfoldAdminEmailInputWidget

from amiribd.adverts.models import Advert
from amiribd.invest.models import Plan
from amiribd.jobs.models import Job

from .models import Address
from .models import Document
from .models import Profile
from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }
        widgets = {
            "email": UnfoldAdminEmailInputWidget(),
        }


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email Address",
            },
        ),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control fakepassword pe-6",
                "id": "psw-input",
                "placeholder": "Enter your password",
            },
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Remember me?"),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input border",
                "id": "remember-me",
            },
        ),
    )


class AuthTokenCodeForm(forms.Form):
    code = forms.CharField(
        label="Authorization code",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg form-control-outlined",
                "id": "outlined-lg",
                "placeholder": "323433442",
            },
        ),
    )


class EmailSignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username", "autocomplete": ""},
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
            },
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control fakepassword pe-6",
                "id": "psw-input",
                "placeholder": "Enter your password",
            },
        ),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control fakepassword pe-6",
                "id": "psw-input-2",
                "placeholder": "Confirm your password",
            },
        ),
    )
    terms_and_conditions = forms.BooleanField(
        required=True,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input border"},
        ),
        label=_("I agree to all Terms & conditions and the privacy policy."),
    )

    def clean(self):
        value = super().clean()
        if (
            "password" in value
            and "password2" in value
            and value["password"] != value["password2"]
        ):
            msg = "Passwords do not match"
            raise forms.ValidationError(msg)
        return value


class ProfileDetailForm(forms.ModelForm):

    email_address = forms.EmailField(
        disabled=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Email Address",
            },
        ),
    )
    public_username = forms.CharField(
        disabled=False,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Public Username",
            },
        ),
    )

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email_address",
            "date_of_birth",
            "phone_number",
            "public_username",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "First Name",
                },
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Last Name",
                },
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Phone Number",
                    "hx-get": "/kyc/dashboard/kyc/htmx/validation/validate-unique-phone-number/",  # noqa: E501
                    "hx-target": "#phone-number-error-message",
                    "hx-trigger": "keyup changed delay:1s",
                    "hx-swap": "outerHTML",
                    "hx-swap-oob": "true",
                },
            ),
            "date_of_birth": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg date-picker-alt",
                    "placeholder": "2000-04-01",
                    "data-date-format": "yyyy-mm-dd",
                },
            ),
        }


class ProfileAddressForm(forms.ModelForm):
    addr_line2 = forms.CharField(
        required=False,
        label="Address Line 2",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Optional",
            },
        ),
    )

    class Meta:
        model = Address
        fields = [
            "addr_line1",
            "addr_line2",
            "city",
            "state",
            "country",
            "zip_code",
        ]
        labels = {
            "addr_line1": "Address Line 1",
            "country": "Nationality",
        }
        widgets = {
            "addr_line1": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Address line 1",
                },
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "City",
                },
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "State",
                },
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Country",
                },
            ),
            "zip_code": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "zip_code",
                },
            ),
        }


class ProfileVerificationDocumentForm(forms.ModelForm):
    read_terms = forms.BooleanField(
        label="""
        I Have Read The<a href="">
        Terms Of Condition </a> And <a href="">Privacy Policy</a>
        """,
        widget=forms.CheckboxInput(
            attrs={"id": "tc-agree", "class": "custom-control-input"},
        ),
    )
    correct_information = forms.BooleanField(
        label="All The Personal Information I Have Entered Is Correct.",
        widget=forms.CheckboxInput(
            attrs={"id": "info-assure", "class": "custom-control-input"},
        ),
    )

    class Meta:
        model = Document
        fields = ["document_type", "document", "read_terms", "correct_information"]
        widgets = {
            "document": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "style": "width:100%",
                    "margin-top": "22px",
                },
            ),
        }


class AdminProfileForm(forms.ModelForm):

    job_applications = forms.ModelMultipleChoiceField(queryset=Job.objects.all())
    plans = forms.ModelMultipleChoiceField(queryset=Plan.objects.all())
    adverts = forms.ModelMultipleChoiceField(queryset=Advert.objects.all())

    class Meta:
        model = Profile
        fields = "__all__"  # noqa: DJ007
