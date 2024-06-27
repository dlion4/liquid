from django import forms
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget, UnfoldBooleanSwitchWidget, UnfoldAdminFileFieldWidget
from unfold.contrib.forms.widgets import WysiwygWidget
from amiribd.users.models import Profile
from .models import Issue


class AdminIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "profile",
            "title",
            "description",
            "resolved",
            "files",
        ]
        widgets = {
             "profile": UnfoldAdminSelectWidget(choices=Profile.objects.all()),
             "title":UnfoldAdminTextInputWidget(),
             "description": WysiwygWidget(),
             'resolved':UnfoldBooleanSwitchWidget(),
             'files': UnfoldAdminFileFieldWidget()
        }
