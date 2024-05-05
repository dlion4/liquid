from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Full Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})
        self.fields["subject"].widget.attrs.update({"placeholder": "Subject"})
        self.fields["message"].widget.attrs.update({"placeholder": "Message"})

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "uk-input uk-border-rounded"}
            )

        self.fields["message"].widget.attrs.update(
            {"class": "uk-textarea uk-border-rounded", "rows": "6"}
        )
