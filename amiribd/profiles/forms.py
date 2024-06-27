from django import forms

from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget, UnfoldAdminRadioSelectWidget

from amiribd.users.models import Profile
from .models import Agent, PlantformType, Position, Plantform


class AgentForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True,
        widget=forms.RadioSelect(
            attrs={"class": "form-check-input", "id": "customRadio1"}
        ),
    )

    class Meta:
        model = Agent
        fields = ["position"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdminAgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            "profile",
            "position",
            "plantform",
        ]

        widgets = {
            "profile": UnfoldAdminSelectWidget(choices=Profile.objects.all()),
            "position": UnfoldAdminRadioSelectWidget(),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {
            "name":UnfoldAdminTextInputWidget(),
        }


class AdminPlatformTypeForm(forms.ModelForm):
    class Meta:
        model = PlantformType
        fields = "__all__"
        widgets = {
            "name":UnfoldAdminTextInputWidget(),
        }

class PlantformTypeForm(forms.Form):
    plantform_type = forms.ModelMultipleChoiceField(
        queryset=PlantformType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Set to True if the field is mandatory
    )


class PlantformForm(forms.ModelForm):
    platform_type = forms.ModelMultipleChoiceField(
        queryset=PlantformType.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "custom-control-input"}),
        required=False,  # Set to True if the field is mandatory
    )
    plan = forms.ChoiceField(widget=UnfoldAdminSelectWidget(choices=PlantformType.objects.all()))

    class Meta:
        model = Plantform
        fields = ["platform_type", 'plan']  # Replace 'related_field' with the actual field name
        widgets = {
            "platform_type": forms.CheckboxSelectMultiple(),

        }
