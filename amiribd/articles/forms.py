from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article


class ArticleForm(forms.ModelForm):
    """Form for comments to the article."""

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Article Title"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Article
        fields = [
            "content",
            "title",
        ]
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            ),
        }
