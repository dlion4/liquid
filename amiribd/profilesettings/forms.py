from django import forms
from amiribd.profilesettings.models import NotificationType


class NotificationForm(forms.ModelForm):
    notify = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "custom-control-input", "id": "unusual-activity"}
        )
    )

    def __init__(self, *args, **kwargs):
        object_pk = kwargs.pop("object_pk", None)
        super(NotificationForm, self).__init__(*args, **kwargs)
        if object_pk is not None:
            self.fields["notify"].widget.attrs.update(
                {"class": "custom-control-input", "id": f"unusual-activity-{object_pk}"}
            )

    class Meta:
        model = NotificationType
        fields = [
            "notify",
        ]
